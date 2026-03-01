class IRInstruction:
    def __init__(self):
        self.security_label = None


class IRBinaryOp(IRInstruction):
    def __init__(self, target, left, op, right):
        super().__init__()
        self.target = target
        self.left = left
        self.op = op
        self.right = right


class IRAssign(IRInstruction):
    def __init__(self, target, value):
        super().__init__()
        self.target = target
        self.value = value


class IRCall(IRInstruction):
    def __init__(self, target, function, args):
        super().__init__()
        self.target = target
        self.function = function
        self.args = args


class IRReturn(IRInstruction):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IRBranch(IRInstruction):
    def __init__(self, condition, true_block, false_block):
        super().__init__()
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class IRJump(IRInstruction):
    def __init__(self, target_block):
        super().__init__()
        self.target_block = target_block


class IRPhi:
    def __init__(self, target):
        self.target = target
        self.sources = {}  # predecessor_block -> variable_name
        self.security_label = None

    def __repr__(self):
        incoming = ", ".join(
            f"{blk.name}:{var}" for blk, var in self.sources.items()
        )
        return f"{self.target} = phi({incoming})"