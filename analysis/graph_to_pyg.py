import torch
from torch_geometric.data import Data


class GraphToPyGConverter:

    def __init__(self, program_graph):
        self.graph = program_graph

        self.node_type_map = {}
        self.edge_type_map = {}

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def convert(self):

        node_features = []
        node_id_map = {}

        # -------------------------------------------------
        # Assign integer IDs to nodes
        # -------------------------------------------------
        for i, (node_id, node) in enumerate(self.graph.nodes.items()):
            node_id_map[node_id] = i

            node_type_id = self._encode_node_type(node.type)
            security_level = self._encode_security(node.features.get("security_level"))

            node_features.append([node_type_id, security_level])

        x = torch.tensor(node_features, dtype=torch.float)

        # -------------------------------------------------
        # Build edge_index and edge_attr
        # -------------------------------------------------
        edge_index = []
        edge_attr = []

        for edge in self.graph.edges:
            src = node_id_map[edge.source]
            dst = node_id_map[edge.target]

            edge_index.append([src, dst])
            edge_type_id = self._encode_edge_type(edge.type)
            edge_attr.append([edge_type_id])

        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(edge_attr, dtype=torch.float)

        # -------------------------------------------------
        # Return PyG Data object
        # -------------------------------------------------
        data = Data(
            x=x,
            edge_index=edge_index,
            edge_attr=edge_attr
        )

        return data

    # =====================================================
    # Encoding Helpers
    # =====================================================

    def _encode_node_type(self, node_type):

        if node_type not in self.node_type_map:
            self.node_type_map[node_type] = len(self.node_type_map)

        return self.node_type_map[node_type]

    def _encode_edge_type(self, edge_type):

        if edge_type not in self.edge_type_map:
            self.edge_type_map[edge_type] = len(self.edge_type_map)

        return self.edge_type_map[edge_type]

    def _encode_security(self, sec):

        if sec is None:
            return 0

        mapping = {
            "TRUSTED": 0,
            "SANITIZED": 1,
            "UNTRUSTED": 2,
            "TAINTED": 3
        }

        return mapping.get(sec, 0)