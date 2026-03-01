import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class SecureGNN(torch.nn.Module):

    def __init__(self, input_dim=2, hidden_dim=64, output_dim=2):
        super().__init__()

        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)

        self.fc = torch.nn.Linear(hidden_dim, output_dim)

    def forward(self, data):

        x, edge_index = data.x, data.edge_index

        x = self.conv1(x, edge_index)
        x = F.relu(x)

        x = self.conv2(x, edge_index)
        x = F.relu(x)

        x = torch.mean(x, dim=0)  # graph-level pooling

        out = self.fc(x)

        return out