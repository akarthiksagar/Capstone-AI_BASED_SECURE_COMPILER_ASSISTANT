import torch
import hashlib


class GraphTensorizer:

    def __init__(self, opcode_dim=251):
        # Use fixed-size hashed opcode features so every graph has identical
        # node feature width (opcode_dim + security_dim = 256 by default).
        self.opcode_dim = opcode_dim
        self.security_vocab = {
            "None": 0,
            "TRUSTED": 1,
            "UNTRUSTED": 2,
            "SANITIZED": 3,
            "TAINTED": 4
        }
        self.security_dim = len(self.security_vocab)

    # =====================================================
    # Main Entry
    # =====================================================

    def tensorize(self, pdg):
        node_features = []
        edge_index = []
        edge_types = []

        # --------------------------
        # Build Node Feature Matrix
        # --------------------------

        for _, node_obj in pdg.nodes.items():

            opcode = node_obj.features["opcode"]
            sec = node_obj.features["security_level"]

            opcode_vec = self._encode_opcode(opcode)
            sec_vec = self._encode_security(sec)

            feature_vec = opcode_vec + sec_vec
            node_features.append(feature_vec)

        # --------------------------
        # Build Edge Index
        # --------------------------

        for edge in pdg.edges:

            src = edge.source
            dst = edge.target
            edge_type = edge.type

            edge_index.append([src, dst])

            if edge_type == "DATA_DEP":
                edge_types.append(0)
            else:
                edge_types.append(1)

        total_dim = self.opcode_dim + self.security_dim
        if node_features:
            X = torch.tensor(node_features, dtype=torch.float)
        else:
            X = torch.zeros((0, total_dim), dtype=torch.float)

        if edge_index:
            edge_index = torch.tensor(edge_index, dtype=torch.long).t()
            edge_types = torch.tensor(edge_types, dtype=torch.long)
        else:
            edge_index = torch.zeros((2, 0), dtype=torch.long)
            edge_types = torch.zeros((0,), dtype=torch.long)

        return X, edge_index, edge_types

    # =====================================================
    # Vocabulary Builders
    # =====================================================

    def _build_opcode_vocab(self, pdg):
        # No-op retained for backward compatibility.
        return

    # =====================================================
    # Encoders
    # =====================================================

    def _encode_opcode(self, opcode):
        # Stable hash -> fixed bucket index
        opcode_bytes = str(opcode).encode("utf-8", errors="ignore")
        idx = int(hashlib.sha256(opcode_bytes).hexdigest(), 16) % self.opcode_dim
        vec = [0] * self.opcode_dim
        vec[idx] = 1
        return vec

    def _encode_security(self, sec):

        sec_id = self.security_vocab.get(sec, 0)
        vec = [0] * len(self.security_vocab)
        vec[sec_id] = 1
        return vec
