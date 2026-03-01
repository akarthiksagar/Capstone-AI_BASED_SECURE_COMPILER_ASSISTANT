import torch


class GraphTensorizer:

    def __init__(self):
        self.opcode_vocab = {}
        self.security_vocab = {
            "None": 0,
            "TRUSTED": 1,
            "UNTRUSTED": 2,
            "SANITIZED": 3,
            "TAINTED": 4
        }

    # =====================================================
    # Main Entry
    # =====================================================

    def tensorize(self, pdg):

        self._build_opcode_vocab(pdg)

        node_features = []
        edge_index = []
        edge_types = []

        # --------------------------
        # Build Node Feature Matrix
        # --------------------------

        for node_id, node_obj in pdg.nodes.items():

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

        X = torch.tensor(node_features, dtype=torch.float)
        edge_index = torch.tensor(edge_index, dtype=torch.long).t()
        edge_types = torch.tensor(edge_types, dtype=torch.long)

        return X, edge_index, edge_types

    # =====================================================
    # Vocabulary Builders
    # =====================================================

    def _build_opcode_vocab(self, pdg):

        for node_obj in pdg.nodes.values():
            opcode = node_obj.features["opcode"]
            if opcode not in self.opcode_vocab:
                self.opcode_vocab[opcode] = len(self.opcode_vocab)

    # =====================================================
    # Encoders
    # =====================================================

    def _encode_opcode(self, opcode):

        vec = [0] * len(self.opcode_vocab)
        idx = self.opcode_vocab[opcode]
        vec[idx] = 1
        return vec

    def _encode_security(self, sec):

        sec_id = self.security_vocab.get(sec, 0)
        vec = [0] * len(self.security_vocab)
        vec[sec_id] = 1
        return vec