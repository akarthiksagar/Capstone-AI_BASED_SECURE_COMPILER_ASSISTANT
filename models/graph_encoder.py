import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool


class GraphEncoder(torch.nn.Module):

    def __init__(self, input_dim=2, hidden_dim=128):
        super().__init__()

        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)

    def forward(self, data):

        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)

        x = self.conv2(x, edge_index)
        x = F.relu(x)

        # Batch-aware pooling
        if hasattr(data, "batch"):
            x = global_mean_pool(x, data.batch)
        else:
            x = torch.mean(x, dim=0, keepdim=True)

        return x