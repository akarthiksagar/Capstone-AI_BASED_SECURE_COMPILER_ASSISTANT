from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field

from ..ir import (
    IRProgram, IRFunction, IRInstruction, IROpCode,
    IRTemp, IRConst, IRVar, IRLabel, IRValue
)
from ...utils.errors import SecurityIssue, Severity


DANGEROUS_FUNCTIONS = {
    'eval': ('Code Injection', Severity.CRITICAL, 'CWE-94'),
    'exec': ('Code Injection', Severity.CRITICAL, 'CWE-94'),
    'compile': ('Code Compilation', Severity.HIGH, 'CWE-94'),
    'system': ('Command Injection', Severity.CRITICAL, 'CWE-78'),
    'popen': ('Command Injection', Severity.CRITICAL, 'CWE-78'),
    'spawn': ('Command Injection', Severity.HIGH, 'CWE-78'),
    'loads': ('Insecure Deserialization', Severity.CRITICAL, 'CWE-502'),
    'load': ('Insecure Deserialization', Severity.HIGH, 'CWE-502'),
}

OBFUSCATION_PATTERNS = [
    ('ev', 'al'),
    ('ex', 'ec'),
    ('sys', 'tem'),
    ('lo', 'ads'),
    ('com', 'pile'),
]


@dataclass
class DeobfuscationResult:
    original_value: str
    resolved_value: str
    is_dangerous: bool
    line: int
    security_issue: Optional[SecurityIssue] = None


class DeobfuscationPass:

    def __init__(self):
        self.security_issues: List[SecurityIssue] = []
        self.resolved_strings: Dict[str, DeobfuscationResult] = {}
        self.string_variables: Dict[str, str] = {}

    def analyze(self, program: IRProgram) -> Tuple[IRProgram, List[SecurityIssue]]:
        self.security_issues = []
        self.resolved_strings = {}
        self.string_variables = {}

        self._analyze_instructions(program.global_instructions)

        for func in program.functions:
            self.string_variables = {}
            self._analyze_instructions(func.instructions)

        return program, self.security_issues

    def _analyze_instructions(self, instructions: List[IRInstruction]) -> None:
        for instr in instructions:
            if instr.opcode == IROpCode.ASSIGN:
                if isinstance(instr.dest, (IRVar, IRTemp)):
                    dest_name = self._get_name(instr.dest)

                    if isinstance(instr.arg1, IRConst) and instr.arg1.value_type == "string":
                        value = instr.arg1.value
                        self.string_variables[dest_name] = value

                        if instr.metadata.get('was_concat') or instr.metadata.get('folded'):
                            self._check_dangerous_string(value, instr.line)

            if instr.opcode == IROpCode.CALL:
                self._check_call_obfuscation(instr)

    def _check_dangerous_string(self, value: str, line: int) -> None:
        value_lower = value.lower()

        for dangerous_name, (desc, severity, cwe) in DANGEROUS_FUNCTIONS.items():
            if value_lower == dangerous_name:
                issue = SecurityIssue(
                    name=f"Obfuscated {dangerous_name}",
                    severity=severity,
                    line=line,
                    column=0,
                    description=f"De-obfuscation detected: String resolves to '{dangerous_name}' - {desc}",
                    recommendation="Avoid dynamic construction of dangerous function names. Use safe alternatives.",
                    cwe_id=cwe,
                    phase="Middle-End"
                )
                self.security_issues.append(issue)

                self.resolved_strings[value] = DeobfuscationResult(
                    original_value="<concatenated>",
                    resolved_value=value,
                    is_dangerous=True,
                    line=line,
                    security_issue=issue
                )
                return

    def _check_call_obfuscation(self, instr: IRInstruction) -> None:
        if not instr.arg1:
            return

        func_name = None

        if isinstance(instr.arg1, (IRVar, IRTemp)):
            var_name = self._get_name(instr.arg1)
            if var_name in self.string_variables:
                func_name = self.string_variables[var_name]

        if func_name:
            self._check_dangerous_string(func_name, instr.line)

    def _get_name(self, value: IRValue) -> str:
        if isinstance(value, IRVar):
            return value.name
        elif isinstance(value, IRTemp):
            return f"t{value.name}"
        return ""

    def get_issues(self) -> List[SecurityIssue]:
        return self.security_issues


class StringConcatAnalyzer:

    def __init__(self):
        self.concat_operations: List[Dict] = []

    def analyze(self, instructions: List[IRInstruction]) -> List[Dict]:
        self.concat_operations = []

        for i, instr in enumerate(instructions):
            if instr.opcode == IROpCode.ADD:
                if self._could_be_string_concat(instr):
                    self.concat_operations.append({
                        'index': i,
                        'instruction': instr,
                        'line': instr.line
                    })

        return self.concat_operations

    def _could_be_string_concat(self, instr: IRInstruction) -> bool:
        if isinstance(instr.arg1, IRConst) and instr.arg1.value_type == "string":
            return True
        if isinstance(instr.arg2, IRConst) and instr.arg2.value_type == "string":
            return True
        return False
