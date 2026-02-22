from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from .ir import (
    IRProgram, IRFunction, IRInstruction, IROpCode,
    IRTemp, IRConst, IRVar, IRLabel, IRValue
)
from .optimization.deobfuscation import DeobfuscationPass
from .optimization.constant_propagation import ConstantPropagation
from ..utils.errors import SecurityIssue, Severity, CompilationResult


class TaintSource(Enum):
    USER_INPUT = "user_input"
    FILE_READ = "file_read"
    NETWORK = "network"
    ENVIRONMENT = "environment"
    UNKNOWN = "unknown"


@dataclass
class TaintInfo:
    is_tainted: bool = False
    source: TaintSource = TaintSource.UNKNOWN
    line: int = 0
    propagation_path: List[int] = field(default_factory=list)


class MiddleEndSecurityAnalyzer:

    TAINT_SOURCES = {
        'input': TaintSource.USER_INPUT,
        'read': TaintSource.FILE_READ,
        'recv': TaintSource.NETWORK,
        'getenv': TaintSource.ENVIRONMENT,
        'raw_input': TaintSource.USER_INPUT,
    }

    DANGEROUS_SINKS = {
        'eval': 'Code Injection via tainted data',
        'exec': 'Code Injection via tainted data',
        'system': 'Command Injection via tainted data',
        'popen': 'Command Injection via tainted data',
        'call': 'Potential Command Injection',
        'execute': 'Potential SQL Injection',
        'loads': 'Insecure Deserialization of tainted data',
    }

    def __init__(self):
        self.taint_map: Dict[str, TaintInfo] = {}
        self.security_issues: List[SecurityIssue] = []
        self.const_prop = ConstantPropagation()
        self.deobfuscation = DeobfuscationPass()

    def analyze(self, program: IRProgram) -> CompilationResult:
        result = CompilationResult(success=True)
        self.security_issues = []

        program = self.const_prop.optimize(program)

        _, deobfusc_issues = self.deobfuscation.analyze(program)
        for issue in deobfusc_issues:
            self.security_issues.append(issue)

        self.taint_map = {}
        self._analyze_taint(program.global_instructions)

        for func in program.functions:
            self.taint_map = {}
            for param in func.parameters:
                self.taint_map[param] = TaintInfo(
                    is_tainted=True,
                    source=TaintSource.UNKNOWN
                )
            self._analyze_taint(func.instructions)

        for issue in self.security_issues:
            result.add_security_issue(issue)

        return result

    def _analyze_taint(self, instructions: List[IRInstruction]) -> None:
        for instr in instructions:
            if instr.opcode == IROpCode.CALL:
                self._check_taint_source(instr)
                self._check_tainted_sink(instr)

            elif instr.opcode == IROpCode.ASSIGN:
                self._propagate_taint_assign(instr)

            elif instr.opcode in [IROpCode.ADD, IROpCode.SUB, IROpCode.MUL,
                                   IROpCode.DIV, IROpCode.MOD]:
                self._propagate_taint_binary(instr)

            elif instr.opcode == IROpCode.INDEX:
                self._propagate_taint_index(instr)

    def _check_taint_source(self, instr: IRInstruction) -> None:
        if not isinstance(instr.arg1, (IRVar, IRTemp)):
            return

        func_name = self._get_name(instr.arg1)

        if func_name in self.TAINT_SOURCES:
            source = self.TAINT_SOURCES[func_name]

            if instr.dest:
                dest_name = self._get_name(instr.dest)
                self.taint_map[dest_name] = TaintInfo(
                    is_tainted=True,
                    source=source,
                    line=instr.line
                )

    def _check_tainted_sink(self, instr: IRInstruction) -> None:
        if not isinstance(instr.arg1, (IRVar, IRTemp)):
            return

        func_name = self._get_name(instr.arg1)

        if func_name in self.DANGEROUS_SINKS:
            args = instr.metadata.get('args', [])

            for arg in args:
                if isinstance(arg, (IRVar, IRTemp)):
                    arg_name = self._get_name(arg)

                    if arg_name in self.taint_map and self.taint_map[arg_name].is_tainted:
                        taint_info = self.taint_map[arg_name]

                        issue = SecurityIssue(
                            name=f"Tainted {func_name}",
                            severity=Severity.CRITICAL,
                            line=instr.line,
                            column=0,
                            description=f"{self.DANGEROUS_SINKS[func_name]}: Tainted data from {taint_info.source.value} flows to {func_name}()",
                            recommendation="Validate and sanitize all user input before use in sensitive functions.",
                            cwe_id="CWE-20",
                            phase="Middle-End"
                        )
                        self.security_issues.append(issue)

    def _propagate_taint_assign(self, instr: IRInstruction) -> None:
        if not instr.dest:
            return

        dest_name = self._get_name(instr.dest)

        if isinstance(instr.arg1, (IRVar, IRTemp)):
            src_name = self._get_name(instr.arg1)

            if src_name in self.taint_map and self.taint_map[src_name].is_tainted:
                src_info = self.taint_map[src_name]
                self.taint_map[dest_name] = TaintInfo(
                    is_tainted=True,
                    source=src_info.source,
                    line=instr.line,
                    propagation_path=src_info.propagation_path + [instr.line]
                )
                return

        if isinstance(instr.arg1, IRConst):
            if dest_name in self.taint_map:
                del self.taint_map[dest_name]

    def _propagate_taint_binary(self, instr: IRInstruction) -> None:
        if not instr.dest:
            return

        dest_name = self._get_name(instr.dest)
        tainted = False
        source = TaintSource.UNKNOWN
        path = []

        for arg in [instr.arg1, instr.arg2]:
            if isinstance(arg, (IRVar, IRTemp)):
                arg_name = self._get_name(arg)
                if arg_name in self.taint_map and self.taint_map[arg_name].is_tainted:
                    tainted = True
                    source = self.taint_map[arg_name].source
                    path = self.taint_map[arg_name].propagation_path

        if tainted:
            self.taint_map[dest_name] = TaintInfo(
                is_tainted=True,
                source=source,
                line=instr.line,
                propagation_path=path + [instr.line]
            )

    def _propagate_taint_index(self, instr: IRInstruction) -> None:
        if not instr.dest:
            return

        dest_name = self._get_name(instr.dest)

        if isinstance(instr.arg1, (IRVar, IRTemp)):
            base_name = self._get_name(instr.arg1)
            if base_name in self.taint_map and self.taint_map[base_name].is_tainted:
                self.taint_map[dest_name] = TaintInfo(
                    is_tainted=True,
                    source=self.taint_map[base_name].source,
                    line=instr.line
                )

    def _get_name(self, value: IRValue) -> str:
        if isinstance(value, IRVar):
            return value.name
        elif isinstance(value, IRTemp):
            return f"t{value.name}"
        elif isinstance(value, IRConst):
            return str(value.value)
        return ""

    def get_optimized_program(self) -> Optional[IRProgram]:
        return None
