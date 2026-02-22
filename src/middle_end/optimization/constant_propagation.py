from typing import Dict, Optional, Any, List, Set
from dataclasses import dataclass

from ..ir import (
    IRProgram, IRFunction, IRInstruction, IROpCode,
    IRTemp, IRConst, IRVar, IRLabel, IRValue
)


@dataclass
class ValueInfo:
    is_constant: bool
    value: Any = None
    value_type: str = "unknown"


class ConstantPropagation:

    def __init__(self):
        self.constants: Dict[str, ValueInfo] = {}
        self.changed: bool = False

    def optimize(self, program: IRProgram) -> IRProgram:
        self.constants = {}

        program.global_instructions = self._process_instructions(program.global_instructions)

        for func in program.functions:
            self.constants = {}
            func.instructions = self._process_instructions(func.instructions)

        return program

    def _process_instructions(self, instructions: List[IRInstruction]) -> List[IRInstruction]:
        result = []

        for instr in instructions:
            optimized = self._optimize_instruction(instr)
            if optimized:
                result.append(optimized)

        return result

    def _optimize_instruction(self, instr: IRInstruction) -> Optional[IRInstruction]:

        if instr.opcode == IROpCode.ASSIGN:
            if isinstance(instr.dest, (IRVar, IRTemp)):
                dest_name = self._get_name(instr.dest)

                if isinstance(instr.arg1, IRConst):
                    self.constants[dest_name] = ValueInfo(
                        is_constant=True,
                        value=instr.arg1.value,
                        value_type=instr.arg1.value_type
                    )
                elif isinstance(instr.arg1, (IRVar, IRTemp)):
                    source_name = self._get_name(instr.arg1)
                    if source_name in self.constants and self.constants[source_name].is_constant:
                        info = self.constants[source_name]
                        self.constants[dest_name] = info
                        return IRInstruction(
                            IROpCode.ASSIGN,
                            dest=instr.dest,
                            arg1=IRConst(info.value, info.value_type),
                            line=instr.line,
                            metadata=instr.metadata
                        )
                else:
                    if dest_name in self.constants:
                        del self.constants[dest_name]

        if instr.opcode in [IROpCode.ADD, IROpCode.SUB, IROpCode.MUL,
                            IROpCode.DIV, IROpCode.MOD, IROpCode.POW]:
            left_const = self._get_constant(instr.arg1)
            right_const = self._get_constant(instr.arg2)

            if left_const is not None and right_const is not None:
                try:
                    result = self._fold_arithmetic(instr.opcode, left_const, right_const)
                    if result is not None:
                        dest_name = self._get_name(instr.dest)
                        value_type = "float" if isinstance(result, float) else "int"
                        self.constants[dest_name] = ValueInfo(True, result, value_type)

                        return IRInstruction(
                            IROpCode.ASSIGN,
                            dest=instr.dest,
                            arg1=IRConst(result, value_type),
                            line=instr.line,
                            metadata={'folded': True}
                        )
                except:
                    pass

        if instr.opcode == IROpCode.ADD:
            left_const = self._get_constant(instr.arg1)
            right_const = self._get_constant(instr.arg2)

            if isinstance(left_const, str) and isinstance(right_const, str):
                result = left_const + right_const
                dest_name = self._get_name(instr.dest)
                self.constants[dest_name] = ValueInfo(True, result, "string")

                return IRInstruction(
                    IROpCode.ASSIGN,
                    dest=instr.dest,
                    arg1=IRConst(result, "string"),
                    line=instr.line,
                    metadata={'folded': True, 'was_concat': True}
                )

        if instr.opcode in [IROpCode.LT, IROpCode.GT, IROpCode.LE,
                            IROpCode.GE, IROpCode.EQ, IROpCode.NE]:
            left_const = self._get_constant(instr.arg1)
            right_const = self._get_constant(instr.arg2)

            if left_const is not None and right_const is not None:
                try:
                    result = self._fold_comparison(instr.opcode, left_const, right_const)
                    dest_name = self._get_name(instr.dest)
                    self.constants[dest_name] = ValueInfo(True, result, "bool")

                    return IRInstruction(
                        IROpCode.ASSIGN,
                        dest=instr.dest,
                        arg1=IRConst(result, "bool"),
                        line=instr.line,
                        metadata={'folded': True}
                    )
                except:
                    pass

        if instr.opcode == IROpCode.NEG:
            operand_const = self._get_constant(instr.arg1)
            if operand_const is not None and isinstance(operand_const, (int, float)):
                result = -operand_const
                dest_name = self._get_name(instr.dest)
                value_type = "float" if isinstance(result, float) else "int"
                self.constants[dest_name] = ValueInfo(True, result, value_type)

                return IRInstruction(
                    IROpCode.ASSIGN,
                    dest=instr.dest,
                    arg1=IRConst(result, value_type),
                    line=instr.line,
                    metadata={'folded': True}
                )

        if instr.opcode == IROpCode.NOT:
            operand_const = self._get_constant(instr.arg1)
            if operand_const is not None:
                result = not operand_const
                dest_name = self._get_name(instr.dest)
                self.constants[dest_name] = ValueInfo(True, result, "bool")

                return IRInstruction(
                    IROpCode.ASSIGN,
                    dest=instr.dest,
                    arg1=IRConst(result, "bool"),
                    line=instr.line,
                    metadata={'folded': True}
                )

        instr = self._propagate_operands(instr)
        return instr

    def _propagate_operands(self, instr: IRInstruction) -> IRInstruction:
        new_arg1 = instr.arg1
        new_arg2 = instr.arg2

        if isinstance(instr.arg1, (IRVar, IRTemp)):
            name = self._get_name(instr.arg1)
            if name in self.constants and self.constants[name].is_constant:
                info = self.constants[name]
                new_arg1 = IRConst(info.value, info.value_type)

        if isinstance(instr.arg2, (IRVar, IRTemp)):
            name = self._get_name(instr.arg2)
            if name in self.constants and self.constants[name].is_constant:
                info = self.constants[name]
                new_arg2 = IRConst(info.value, info.value_type)

        if new_arg1 is not instr.arg1 or new_arg2 is not instr.arg2:
            return IRInstruction(
                instr.opcode,
                dest=instr.dest,
                arg1=new_arg1,
                arg2=new_arg2,
                line=instr.line,
                metadata=instr.metadata
            )

        return instr

    def _get_name(self, value: IRValue) -> str:
        if isinstance(value, IRVar):
            return value.name
        elif isinstance(value, IRTemp):
            return f"t{value.name}"
        return ""

    def _get_constant(self, value: IRValue) -> Optional[Any]:
        if isinstance(value, IRConst):
            return value.value

        if isinstance(value, (IRVar, IRTemp)):
            name = self._get_name(value)
            if name in self.constants and self.constants[name].is_constant:
                return self.constants[name].value

        return None

    def _fold_arithmetic(self, opcode: IROpCode, left: Any, right: Any) -> Optional[Any]:
        try:
            if opcode == IROpCode.ADD:
                return left + right
            elif opcode == IROpCode.SUB:
                return left - right
            elif opcode == IROpCode.MUL:
                return left * right
            elif opcode == IROpCode.DIV:
                if right == 0:
                    return None
                return left / right
            elif opcode == IROpCode.MOD:
                if right == 0:
                    return None
                return left % right
            elif opcode == IROpCode.POW:
                return left ** right
        except:
            return None
        return None

    def _fold_comparison(self, opcode: IROpCode, left: Any, right: Any) -> bool:
        if opcode == IROpCode.LT:
            return left < right
        elif opcode == IROpCode.GT:
            return left > right
        elif opcode == IROpCode.LE:
            return left <= right
        elif opcode == IROpCode.GE:
            return left >= right
        elif opcode == IROpCode.EQ:
            return left == right
        elif opcode == IROpCode.NE:
            return left != right
        return False
