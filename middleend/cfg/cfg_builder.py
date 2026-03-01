from middleend.cfg.basic_block import BasicBlock


class ControlFlowGraph:

    def __init__(self):
        self.blocks = []
        self.entry = None
        self.exit = None
        self.block_counter = 0

    # ------------------------------------------------------
    # Create new block
    # ------------------------------------------------------

    def new_block(self, name_prefix="block"):
        name = f"{name_prefix}_{self.block_counter}"
        self.block_counter += 1

        block = BasicBlock(name)
        self.blocks.append(block)

        if self.entry is None:
            self.entry = block

        return block

    # ------------------------------------------------------
    # Set exit block
    # ------------------------------------------------------

    def set_exit(self, block):
        self.exit = block

    # ------------------------------------------------------
    # Add edge
    # ------------------------------------------------------

    def add_edge(self, from_block, to_block):
        from_block.add_successor(to_block)

    # ------------------------------------------------------
    # Utility: iterate blocks
    # ------------------------------------------------------

    def __iter__(self):
        return iter(self.blocks)

    # ------------------------------------------------------
    # Debug printing
    # ------------------------------------------------------

    def dump(self):
        for block in self.blocks:
            print(f"Block {block.name}")
            for instr in block.instructions:
                print("   ", instr)
            for succ in block.successors:
                print(f"    → {succ.name}")