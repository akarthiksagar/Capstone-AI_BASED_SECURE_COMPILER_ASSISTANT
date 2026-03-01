from collections import defaultdict

from analysis.control_dependence import ControlDependenceGraph
from analysis.graph_representation import ProgramGraph
from middleend.ir.ir_instructions import IRBranch


class PDGBuilder:

    def __init__(self, cfg):
        self.cfg = cfg
        self.pdg = ProgramGraph()

        # instruction → node_id
        self.instr_nodes = {}

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def build(self):

        self._add_instruction_nodes()
        self._add_data_dependencies()
        self._add_control_dependencies()

        return self.pdg

    # =====================================================
    # Instruction Nodes
    # =====================================================

    def _add_instruction_nodes(self):

        for block in self.cfg.blocks:
            for instr in block.instructions:

                node_id = self.pdg.new_node(
                    "Instruction",
                    features={
                        "opcode": instr.__class__.__name__,
                        "security_level": str(getattr(instr, "security_label", None))
                    }
                )

                self.instr_nodes[instr] = node_id

    # =====================================================
    # DATA DEPENDENCIES (SSA-Based)
    # =====================================================

    def _add_data_dependencies(self):

        definition_map = {}

        for block in self.cfg.blocks:
            for instr in block.instructions:

                instr_node = self.instr_nodes[instr]

                # ------------------------
                # Definition
                # ------------------------
                if hasattr(instr, "target"):
                    definition_map[instr.target] = instr_node

                # ------------------------
                # Direct attribute uses
                # ------------------------
                for attr in ["left", "right", "value"]:
                    if hasattr(instr, attr):
                        val = getattr(instr, attr)
                        if isinstance(val, str) and val in definition_map:

                            def_node = definition_map[val]

                            self.pdg.add_edge(
                                def_node,
                                instr_node,
                                "DATA_DEP"
                            )

                # ------------------------
                # Function arguments
                # ------------------------
                if hasattr(instr, "args"):
                    for arg in instr.args:
                        if isinstance(arg, str) and arg in definition_map:

                            def_node = definition_map[arg]

                            self.pdg.add_edge(
                                def_node,
                                instr_node,
                                "DATA_DEP"
                            )

                # ------------------------
                # Phi nodes
                # ------------------------
                if hasattr(instr, "sources"):
                    for var in instr.sources.values():
                        if var in definition_map:
                            def_node = definition_map[var]
                            self.pdg.add_edge(
                                def_node,
                                instr_node,
                                "DATA_DEP"
                            )

    # =====================================================
    # CONTROL DEPENDENCIES (CDG-Based)
    # =====================================================

    def _add_control_dependencies(self):

        cdg = ControlDependenceGraph(self.cfg)
        control_deps = cdg.compute()

        for src_block, dst_blocks in control_deps.items():

            # Only branch instruction is control source
            branch_instr = None
            for instr in src_block.instructions:
                if isinstance(instr, IRBranch):
                    branch_instr = instr
                    break

            if branch_instr is None:
                continue

            src_id = self.instr_nodes[branch_instr]

            for dst_block in dst_blocks:
                for instr in dst_block.instructions:

                    dst_id = self.instr_nodes[instr]

                    self.pdg.add_edge(
                        src_id,
                        dst_id,
                        "CONTROL_DEP"
                    )