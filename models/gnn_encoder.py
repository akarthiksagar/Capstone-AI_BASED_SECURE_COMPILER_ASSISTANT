import torch
import torch.nn as nn
import torch.nn.functional as F


# =========================================================
# Custom Edge-Type Aware GNN Layer
# =========================================================

class EdgeTypeGNNLayer(nn.Module):

    def __init__(self, in_dim, out_dim):
        super().__init__()

        self.W_data = nn.Linear(in_dim, out_dim)
        self.W_control = nn.Linear(in_dim, out_dim)
        self.W_self = nn.Linear(in_dim, out_dim)

    def forward(self, X, edge_index, edge_types):

        num_nodes = X.size(0)
        out = torch.zeros(num_nodes, self.W_self.out_features, device=X.device)

        src_nodes = edge_index[0]
        dst_nodes = edge_index[1]

        for i in range(edge_index.size(1)):

            src = src_nodes[i]
            dst = dst_nodes[i]
            edge_type = edge_types[i]

            if edge_type == 0:   # DATA_DEP
                message = self.W_data(X[src])
            else:                # CONTROL_DEP
                message = self.W_control(X[src])

            out[dst] += message

        # Self transformation
        out += self.W_self(X)

        return F.relu(out)


# =========================================================
# Full SecureGNN Encoder
# =========================================================

class SecureGNN(nn.Module):

    def __init__(self, input_dim, hidden_dim=64, num_layers=3):
        super().__init__()

        self.layers = nn.ModuleList()

        # First layer
        self.layers.append(EdgeTypeGNNLayer(input_dim, hidden_dim))

        # Hidden layers
        for _ in range(num_layers - 1):
            self.layers.append(EdgeTypeGNNLayer(hidden_dim, hidden_dim))

        self.hidden_dim = hidden_dim

    # -----------------------------------------------------
    # Graph Forward
    # -----------------------------------------------------

    def forward(self, X, edge_index, edge_types, batch_ids):

        for layer in self.layers:
            X = layer(X, edge_index, edge_types)

        graph_embedding = self._global_mean_pool(X, batch_ids)

        return graph_embedding

    # -----------------------------------------------------
    # Manual Global Mean Pool (Batch Safe)
    # -----------------------------------------------------

    def _global_mean_pool(self, X, batch_ids):

        num_graphs = batch_ids.max().item() + 1
        graph_embeddings = []

        for g in range(num_graphs):
            mask = (batch_ids == g)
            graph_embeddings.append(X[mask].mean(dim=0))

        return torch.stack(graph_embeddings)