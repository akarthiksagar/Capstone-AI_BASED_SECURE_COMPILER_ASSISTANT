from analysis.graph_representation import ProgramGraph
from middleend.ir.ir_instructions import (
    IRBinaryOp,
    IRAssign,
    IRCall,
    IRReturn,
    IRPhi
)


class GraphExtractor:

    def __init__(self, cfg):
        self.cfg = cfg
        self.graph = ProgramGraph()
        self.block_nodes = {}
        self.instruction_nodes = {}
        self.variable_nodes = {}

    # =====================================================
    # Entry Point
    # =====================================================

    def extract(self):
        self._add_blocks()
        self._add_instructions()
        self._add_control_flow_edges()
        self._add_data_flow_edges()
        return self.graph

    # =====================================================
    # Add Basic Blocks
    # =====================================================

    def _add_blocks(self):
        for block in self.cfg.blocks:
            node_id = self.graph.new_node(
                "BasicBlock",
                features={"name": block.name}
            )
            self.block_nodes[block] = node_id

    # =====================================================
    # Add Instructions
    # =====================================================

    def _add_instructions(self):
        for block in self.cfg.blocks:
            block_node = self.block_nodes[block]

            for instr in block.instructions:

                instr_node = self.graph.new_node(
                    "Instruction",
                    features={
                        "opcode": instr.__class__.__name__,
                        "security_level": str(instr.security_label)
                    }
                )

                self.instruction_nodes[instr] = instr_node

                # Link instruction to block
                self.graph.add_edge(
                    block_node,
                    instr_node,
                    "CONTAINS"
                )

    # =====================================================
    # Control Flow Edges
    # =====================================================

    def _add_control_flow_edges(self):
        for block in self.cfg.blocks:
            src_block_node = self.block_nodes[block]

            for succ in block.successors:
                dst_block_node = self.block_nodes[succ]

                self.graph.add_edge(
                    src_block_node,
                    dst_block_node,
                    "CONTROL_FLOW"
                )

    # =====================================================
    # Data Flow Edges (SSA)
    # =====================================================

    def _add_data_flow_edges(self):
        for block in self.cfg.blocks:
            for instr in block.instructions:

                instr_node = self.instruction_nodes[instr]

                # Target variable
                if hasattr(instr, "target"):
                    var_node = self._get_variable_node(instr.target)

                    self.graph.add_edge(
                        instr_node,
                        var_node,
                        "DEFINES"
                    )

                # Operands
                for attr in ["left", "right", "value"]:
                    if hasattr(instr, attr):
                        val = getattr(instr, attr)
                        if isinstance(val, str):
                            var_node = self._get_variable_node(val)

                            self.graph.add_edge(
                                var_node,
                                instr_node,
                                "USES"
                            )

                # Function call arguments
                if hasattr(instr, "args"):
                    for arg in instr.args:
                        if isinstance(arg, str):
                            var_node = self._get_variable_node(arg)

                            self.graph.add_edge(
                                var_node,
                                instr_node,
                                "ARGUMENT"
                            )

    # =====================================================
    # Variable Nodes
    # =====================================================

    def _get_variable_node(self, var_name):
        if var_name not in self.variable_nodes:
            node_id = self.graph.new_node(
                "Variable",
                features={"name": var_name}
            )
            self.variable_nodes[var_name] = node_id

        return self.variable_nodes[var_name]