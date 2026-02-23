# src/frontend/llm_security_checker.py
from dataclasses import dataclass
from typing import List
import re

from ..utils.errors import SecurityIssue, Severity


@dataclass
class FrontendLLMSecurityChecker:

    alias_import_pattern = re.compile(r"import\s+(os|subprocess|pickle|yaml)\s+as\s+([A-Za-z_][A-Za-z0-9_]*)")
    dangerous_member_pattern = re.compile(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*(system|popen|call|run|Popen|check_output|check_call|loads|load)\s*\(",
        re.MULTILINE,
    )

    def analyze(self, source: str) -> List[SecurityIssue]:
        issues: List[SecurityIssue] = []

        alias_map = {}
        for m in self.alias_import_pattern.finditer(source):
            alias_map[m.group(2)] = m.group(1)

        lines = source.splitlines()
        for line_no, text in enumerate(lines, start=1):
            for m in self.dangerous_member_pattern.finditer(text):
                alias = m.group(1)
                member = m.group(2)
                module = alias_map.get(alias)
                if not module:
                    continue

                issues.append(
                    SecurityIssue(
                        name=f"LLM-obfuscated call: {alias}.{member}",
                        severity=Severity.HIGH,
                        line=line_no,
                        column=max(m.start(1), 0),
                        description=(
                            f"Potential obfuscated dangerous call detected via alias import ({module} as {alias})."
                        ),
                        recommendation="Avoid aliasing dangerous modules in security-sensitive code and validate command/data flow.",
                        cwe_id="CWE-78" if module in {"os", "subprocess"} else "CWE-502",
                        phase="Frontend",
                    )
                )

        return issues
