# src/middle_end/llm_ir_security_analyzer.py
from dataclasses import dataclass
from typing import List, Dict, Tuple

from .ir import IRProgram, IRInstruction, IROpCode, IRTemp, IRVar
from ..utils.errors import SecurityIssue, Severity


@dataclass
class IRFinding:
    issue: SecurityIssue


class LLMIRSecurityAnalyzer:

    RISKY_MEMBERS = {"system", "popen", "run", "call", "Popen", "loads", "load", "execute"}

    def analyze(self, program: IRProgram) -> List[SecurityIssue]:
        issues: List[SecurityIssue] = []

        issues.extend(self._scan_instructions(program.global_instructions))
        for func in program.functions:
            issues.extend(self._scan_instructions(func.instructions))

        return issues

    def _scan_instructions(self, instructions: List[IRInstruction]) -> List[SecurityIssue]:
        issues: List[SecurityIssue] = []
        member_temp_to_name: Dict[str, Tuple[str, int, int]] = {}

        for instr in instructions:
            if instr.opcode == IROpCode.MEMBER and isinstance(instr.dest, IRTemp):
                member = getattr(instr.arg2, "name", str(instr.arg2))
                if member in self.RISKY_MEMBERS:
                    src_line = instr.metadata.get("source_line", instr.line)
                    src_col = instr.metadata.get("source_column", 0)
                    member_temp_to_name[instr.dest.name] = (member, src_line, src_col)

            if instr.opcode == IROpCode.CALL and isinstance(instr.arg1, IRTemp):
                info = member_temp_to_name.get(instr.arg1.name)
                if not info:
                    continue

                member, src_line, src_col = info
                issues.append(
                    SecurityIssue(
                        name=f"LLM IR risky indirect call: {member}",
                        severity=Severity.HIGH,
                        line=src_line,
                        column=src_col,
                        description=(
                            "IR-level analyzer detected an indirect/dereferenced call to a risky member; "
                            "this may bypass simple frontend call pattern checks."
                        ),
                        recommendation="Trace data flow to this call target and enforce allow-lists or sanitization.",
                        cwe_id="CWE-78",
                        phase="Middle-End",
                    )
                )

        return issues
