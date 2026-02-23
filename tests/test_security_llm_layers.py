# tests/test_security_llm_layers.py
from src.frontend.llm_security_checker import FrontendLLMSecurityChecker
from src.middle_end.llm_ir_security_analyzer import LLMIRSecurityAnalyzer
from src.middle_end.ir import IRInstruction, IROpCode, IRTemp, IRVar, IRProgram


def test_frontend_llm_checker_detects_alias_obfuscation():
    src = """
import os as o
cmd = input()
o.system(cmd)
""".strip()
    issues = FrontendLLMSecurityChecker().analyze(src)
    assert issues
    assert issues[0].line == 3


def test_ir_llm_checker_maps_member_call_to_source_location():
    member = IRInstruction(
        IROpCode.MEMBER,
        dest=IRTemp("1"),
        arg1=IRVar("o"),
        arg2=IRVar("system"),
        line=10,
        metadata={"source_line": 42, "source_column": 8},
    )
    call = IRInstruction(
        IROpCode.CALL,
        dest=IRTemp("2"),
        arg1=IRTemp("1"),
        line=11,
        metadata={"args": [IRVar("cmd")]},
    )

    program = IRProgram(global_instructions=[member, call])
    issues = LLMIRSecurityAnalyzer().analyze(program)

    assert issues
    assert issues[0].line == 42
    assert issues[0].column == 8
