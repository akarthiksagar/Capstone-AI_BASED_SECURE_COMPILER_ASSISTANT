from dataclasses import dataclass, field
from typing import List, Optional, Any, Union, Dict
from enum import Enum


class IROpCode(Enum):
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    MOD = "mod"
    POW = "pow"
    NEG = "neg"

    LT = "lt"
    GT = "gt"
    LE = "le"
    GE = "ge"
    EQ = "eq"
    NE = "ne"

    AND = "and"
    OR = "or"
    NOT = "not"

    ASSIGN = "assign"
    LOAD = "load"
    STORE = "store"
    COPY = "copy"

    LABEL = "label"
    JUMP = "jump"
    JUMP_IF = "jump_if"
    JUMP_IF_NOT = "jump_if_not"

    CALL = "call"
    RETURN = "return"
    PARAM = "param"
    FUNC_BEGIN = "func_begin"
    FUNC_END = "func_end"

    ALLOC = "alloc"
    INDEX = "index"
    MEMBER = "member"

    NOP = "nop"
    SECURITY_CHECK = "security_check"


@dataclass
class IRValue:
    pass


@dataclass
class IRTemp(IRValue):
    name: str

    def __str__(self) -> str:
        return f"t{self.name}"


@dataclass
class IRConst(IRValue):
    value: Any
    value_type: str = "unknown"

    def __str__(self) -> str:
        if self.value_type == "string":
            return f'"{self.value}"'
        return str(self.value)


@dataclass
class IRVar(IRValue):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class IRLabel(IRValue):
    name: str

    def __str__(self) -> str:
        return f"L{self.name}"


@dataclass
class IRInstruction:
    opcode: IROpCode
    dest: Optional[IRValue] = None
    arg1: Optional[IRValue] = None
    arg2: Optional[IRValue] = None
    line: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        if self.opcode == IROpCode.LABEL:
            return f"{self.dest}:"

        if self.opcode == IROpCode.JUMP:
            return f"    jump {self.dest}"

        if self.opcode == IROpCode.JUMP_IF:
            return f"    if {self.arg1} goto {self.dest}"

        if self.opcode == IROpCode.JUMP_IF_NOT:
            return f"    if not {self.arg1} goto {self.dest}"

        if self.opcode == IROpCode.RETURN:
            if self.arg1:
                return f"    return {self.arg1}"
            return "    return"

        if self.opcode == IROpCode.CALL:
            args = self.metadata.get('args', [])
            args_str = ', '.join(str(a) for a in args)
            if self.dest:
                return f"    {self.dest} = call {self.arg1}({args_str})"
            return f"    call {self.arg1}({args_str})"

        if self.opcode == IROpCode.PARAM:
            return f"    param {self.arg1}"

        if self.opcode == IROpCode.FUNC_BEGIN:
            params = self.metadata.get('params', [])
            return f"func {self.dest}({', '.join(params)}):"

        if self.opcode == IROpCode.FUNC_END:
            return f"end func"

        if self.opcode == IROpCode.ASSIGN:
            return f"    {self.dest} = {self.arg1}"

        if self.opcode == IROpCode.COPY:
            return f"    {self.dest} = {self.arg1}"

        if self.opcode == IROpCode.NEG:
            return f"    {self.dest} = -{self.arg1}"

        if self.opcode == IROpCode.NOT:
            return f"    {self.dest} = not {self.arg1}"

        if self.opcode in [IROpCode.ADD, IROpCode.SUB, IROpCode.MUL,
                           IROpCode.DIV, IROpCode.MOD, IROpCode.POW]:
            op_map = {
                IROpCode.ADD: '+', IROpCode.SUB: '-', IROpCode.MUL: '*',
                IROpCode.DIV: '/', IROpCode.MOD: '%', IROpCode.POW: '**'
            }
            return f"    {self.dest} = {self.arg1} {op_map[self.opcode]} {self.arg2}"

        if self.opcode in [IROpCode.LT, IROpCode.GT, IROpCode.LE,
                           IROpCode.GE, IROpCode.EQ, IROpCode.NE]:
            op_map = {
                IROpCode.LT: '<', IROpCode.GT: '>', IROpCode.LE: '<=',
                IROpCode.GE: '>=', IROpCode.EQ: '==', IROpCode.NE: '!='
            }
            return f"    {self.dest} = {self.arg1} {op_map[self.opcode]} {self.arg2}"

        if self.opcode in [IROpCode.AND, IROpCode.OR]:
            return f"    {self.dest} = {self.arg1} {self.opcode.value} {self.arg2}"

        if self.opcode == IROpCode.INDEX:
            return f"    {self.dest} = {self.arg1}[{self.arg2}]"

        if self.opcode == IROpCode.MEMBER:
            return f"    {self.dest} = {self.arg1}.{self.arg2}"

        if self.opcode == IROpCode.SECURITY_CHECK:
            return f"    SECURITY_CHECK: {self.metadata.get('issue', 'unknown')}"

        return f"    {self.opcode.value} {self.dest} {self.arg1} {self.arg2}"


@dataclass
class IRFunction:
    name: str
    parameters: List[str] = field(default_factory=list)
    instructions: List[IRInstruction] = field(default_factory=list)
    local_vars: Dict[str, IRValue] = field(default_factory=dict)

    def __str__(self) -> str:
        lines = [f"func {self.name}({', '.join(self.parameters)}):"]
        for instr in self.instructions:
            lines.append(str(instr))
        lines.append("end func")
        return '\n'.join(lines)


@dataclass
class IRProgram:
    functions: List[IRFunction] = field(default_factory=list)
    global_instructions: List[IRInstruction] = field(default_factory=list)
    global_vars: Dict[str, IRValue] = field(default_factory=dict)
    constants: Dict[str, IRConst] = field(default_factory=dict)

    def __str__(self) -> str:
        lines = ["=== IR Program ==="]

        if self.global_instructions:
            for instr in self.global_instructions:
                lines.append(str(instr))

        for func in self.functions:
            lines.append("")
            lines.append(str(func))

        return '\n'.join(lines)

    def get_all_instructions(self) -> List[IRInstruction]:
        all_instrs = list(self.global_instructions)
        for func in self.functions:
            all_instrs.extend(func.instructions)
        return all_instrs


class IRBuilder:

    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self) -> IRTemp:
        self.temp_counter += 1
        return IRTemp(name=str(self.temp_counter))

    def new_label(self, prefix: str = "") -> IRLabel:
        self.label_counter += 1
        name = f"{prefix}{self.label_counter}" if prefix else str(self.label_counter)
        return IRLabel(name=name)

    def const(self, value: Any, value_type: str = None) -> IRConst:
        if value_type is None:
            if isinstance(value, str):
                value_type = "string"
            elif isinstance(value, int):
                value_type = "int"
            elif isinstance(value, float):
                value_type = "float"
            elif isinstance(value, bool):
                value_type = "bool"
            else:
                value_type = "unknown"
        return IRConst(value=value, value_type=value_type)

    def var(self, name: str) -> IRVar:
        return IRVar(name=name)

    def assign(self, dest: IRValue, value: IRValue, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.ASSIGN, dest=dest, arg1=value, line=line)

    def binary_op(self, op: str, dest: IRValue, left: IRValue, right: IRValue, line: int = 0) -> IRInstruction:
        op_map = {
            '+': IROpCode.ADD, '-': IROpCode.SUB, '*': IROpCode.MUL,
            '/': IROpCode.DIV, '//': IROpCode.DIV, '%': IROpCode.MOD, '**': IROpCode.POW,
            '<': IROpCode.LT, '>': IROpCode.GT, '<=': IROpCode.LE,
            '>=': IROpCode.GE, '==': IROpCode.EQ, '!=': IROpCode.NE,
            'and': IROpCode.AND, 'or': IROpCode.OR
        }
        opcode = op_map.get(op, IROpCode.NOP)
        return IRInstruction(opcode, dest=dest, arg1=left, arg2=right, line=line)

    def unary_op(self, op: str, dest: IRValue, operand: IRValue, line: int = 0) -> IRInstruction:
        if op == '-':
            return IRInstruction(IROpCode.NEG, dest=dest, arg1=operand, line=line)
        elif op == 'not':
            return IRInstruction(IROpCode.NOT, dest=dest, arg1=operand, line=line)
        return IRInstruction(IROpCode.COPY, dest=dest, arg1=operand, line=line)

    def call(self, dest: Optional[IRValue], func: IRValue, args: List[IRValue], line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.CALL, dest=dest, arg1=func, line=line, metadata={'args': args})

    def label(self, label: IRLabel, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.LABEL, dest=label, line=line)

    def jump(self, label: IRLabel, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.JUMP, dest=label, line=line)

    def jump_if(self, cond: IRValue, label: IRLabel, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.JUMP_IF, dest=label, arg1=cond, line=line)

    def jump_if_not(self, cond: IRValue, label: IRLabel, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.JUMP_IF_NOT, dest=label, arg1=cond, line=line)

    def ret(self, value: Optional[IRValue] = None, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.RETURN, arg1=value, line=line)

    def func_begin(self, name: str, params: List[str], line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.FUNC_BEGIN, dest=IRVar(name), line=line, metadata={'params': params})

    def func_end(self, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.FUNC_END, line=line)

    def index(self, dest: IRValue, base: IRValue, index: IRValue, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.INDEX, dest=dest, arg1=base, arg2=index, line=line)

    def member(self, dest: IRValue, base: IRValue, member: str, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.MEMBER, dest=dest, arg1=base, arg2=IRVar(member), line=line)

    def security_check(self, issue: str, line: int = 0) -> IRInstruction:
        return IRInstruction(IROpCode.SECURITY_CHECK, line=line, metadata={'issue': issue})
