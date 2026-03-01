from middleend.ir.ir_instructions import (
    IRBinaryOp,
    IRAssign,
    IRCall,
    IRReturn,
    IRPhi
)

from frontend.semantic.security_label import SecurityLevel


class IRSecurityAnalyzer:

    def __init__(self, cfg):
        self.cfg = cfg
        self.vulnerabilities = []

    # ======================================================
    # Entry Point
    # ======================================================

    def analyze(self):
        for block in self.cfg.blocks:
            for instr in block.instructions:
                self._analyze_instruction(instr)

        return self.vulnerabilities

    # ======================================================
    # Instruction-Level Analysis
    # ======================================================

    def _analyze_instruction(self, instr):

        if not instr.security_label:
            return

        # Check dangerous calls
        if isinstance(instr, IRCall):
            self._check_call(instr)

        # Return tainted data
        if isinstance(instr, IRReturn):
            self._check_return(instr)

    # ======================================================
    # Tainted Sink Detection
    # ======================================================

    def _check_call(self, instr):

        dangerous_functions = {"exec", "eval", "system", "query"}

        if instr.function in dangerous_functions:

            if instr.security_label.level >= SecurityLevel.UNTRUSTED:
                self.vulnerabilities.append(
                    {
                        "type": "TAINTED_SINK",
                        "function": instr.function,
                        "severity": "HIGH"
                    }
                )

    # ======================================================
    # Tainted Return Detection
    # ======================================================

    def _check_return(self, instr):

        if instr.security_label.level >= SecurityLevel.UNTRUSTED:
            self.vulnerabilities.append(
                {
                    "type": "TAINTED_RETURN",
                    "severity": "MEDIUM"
                }
            )