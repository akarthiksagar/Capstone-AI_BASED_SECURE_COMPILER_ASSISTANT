class BasicBlock:

    def __init__(self, name):
        self.name = name
        self.instructions = []
        self.predecessors = []
        self.successors = []

    def add_instruction(self, instr):
        self.instructions.append(instr)

    def add_successor(self, block):
        if block not in self.successors:
            self.successors.append(block)
            block.predecessors.append(self)