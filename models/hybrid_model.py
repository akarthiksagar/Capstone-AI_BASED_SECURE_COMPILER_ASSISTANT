import torch
import torch.nn as nn
from models.gnn_encoder import SecureGNN
from models.transformer_encoder import CodeBERTEncoder


class HybridModel(nn.Module):

    def __init__(self, graph_input_dim):
        super().__init__()

        self.gnn = SecureGNN(graph_input_dim)
        self.transformer = CodeBERTEncoder()

        fusion_dim = self.gnn.hidden_dim + self.transformer.hidden_size

        self.fusion = nn.Sequential(
            nn.Linear(fusion_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )

    def forward(self, X, edge_index, edge_types, batch_ids, code_list, device):

        graph_embedding = self.gnn(X, edge_index, edge_types, batch_ids)
        transformer_embedding = self.transformer(code_list, device)

        fused = torch.cat([graph_embedding, transformer_embedding], dim=1)

        logits = self.fusion(fused)

        return logits