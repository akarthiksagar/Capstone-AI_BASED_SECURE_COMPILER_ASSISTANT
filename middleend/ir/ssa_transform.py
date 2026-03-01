from collections import defaultdict
from middleend.ir.ir_instructions import IRPhi
from middleend.cfg.dominance import DominanceAnalysis
from analysis.liveness import LivenessAnalysis

class SSATransformer:

    def __init__(self, cfg):
        self.cfg = cfg

        # Dominance structures (external)
        self.idom = {}
        self.dom_tree = {}
        self.dom_frontier = {}

        # SSA structures
        self.version_counter = defaultdict(int)
        self.stacks = defaultdict(list)

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def transform(self):

        # Step 1: Compute dominance using external module
        dom_analysis = DominanceAnalysis(self.cfg)
        self.idom, self.dom_tree, self.dom_frontier = dom_analysis.compute()

        # Step 2: Insert phi nodes
        self._insert_phi_functions()

        # Step 3: Rename variables
        self.rename_variables()

        return self.cfg

    # =====================================================
    # PHI NODE INSERTION
    # =====================================================

    def _insert_phi_functions(self):

        # Compute liveness first
        liveness = LivenessAnalysis(self.cfg)
        live_in, _ = liveness.compute()

        def_sites = {}

        for block in self.cfg.blocks:
            for instr in block.instructions:
                if hasattr(instr, "target"):
                    var = instr.target
                    def_sites.setdefault(var, set()).add(block)

        for var, blocks in def_sites.items():

            worklist = list(blocks)
            placed = set()

            while worklist:
                block = worklist.pop()

                for df_block in self.dom_frontier.get(block, []):

                    # 🔥 PRUNING CONDITION
                    if var not in live_in[df_block]:
                        continue

                    if (df_block, var) not in placed:

                        phi = IRPhi(var)
                        df_block.instructions.insert(0, phi)

                        placed.add((df_block, var))

                        if df_block not in blocks:
                            worklist.append(df_block)
    # =====================================================
    # VARIABLE RENAMING
    # =====================================================

    def new_version(self, var):
        version = self.version_counter[var]
        self.version_counter[var] += 1
        name = f"{var}_{version}"
        self.stacks[var].append(name)
        return name

    def current_name(self, var):
        if self.stacks[var]:
            return self.stacks[var][-1]
        return var

    def rename_variables(self):
        self._rename_block(self.cfg.entry)

    def _rename_block(self, block):

        # Rename phi targets first
        for instr in block.instructions:
            if isinstance(instr, IRPhi):
                new_name = self.new_version(instr.target)
                instr.target = new_name

        # Rename instruction operands and targets
        for instr in block.instructions:

            # Rename operands
            for attr in ["left", "right", "value"]:
                if hasattr(instr, attr):
                    val = getattr(instr, attr)
                    if isinstance(val, str):
                        setattr(instr, attr, self.current_name(val))

            if hasattr(instr, "args"):
                instr.args = [
                    self.current_name(arg) if isinstance(arg, str) else arg
                    for arg in instr.args
                ]

            # Rename target (non-phi)
            if hasattr(instr, "target") and not isinstance(instr, IRPhi):
                new_name = self.new_version(instr.target)
                instr.target = new_name

        # Update phi sources in successors
        for succ in block.successors:
            for instr in succ.instructions:
                if isinstance(instr, IRPhi):
                    base_var = instr.target.split("_")[0]
                    instr.sources[block] = self.current_name(base_var)

        # Recurse along dominator tree
        for child in self.dom_tree.get(block, []):
            self._rename_block(child)

        # Pop stack after finishing block
        for instr in block.instructions:
            if hasattr(instr, "target"):
                base_var = instr.target.split("_")[0]
                if self.stacks[base_var]:
                    self.stacks[base_var].pop()