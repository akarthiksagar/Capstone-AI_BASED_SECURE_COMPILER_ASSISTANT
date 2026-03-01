import torch
import torch.nn as nn
import torch.nn.functional as F

from models.code_encoder import CodeEncoder
from models.graph_encoder import GraphEncoder


class SecureFusionModel(nn.Module):

    def __init__(self, num_classes=2):
        super().__init__()

        self.code_encoder = CodeEncoder()
        self.graph_encoder = GraphEncoder()

        code_dim = 768
        graph_dim = 128

        # Projection layers
        self.code_proj = nn.Linear(code_dim, 256)
        self.graph_proj = nn.Linear(graph_dim, 256)

        # Gating mechanism
        self.gate = nn.Linear(512, 256)

        # Final classifier
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, code_snippet, graph_data):

        code_emb = self.code_encoder(code_snippet)
        graph_emb = self.graph_encoder(graph_data)

        code_emb = F.relu(self.code_proj(code_emb))
        graph_emb = F.relu(self.graph_proj(graph_emb))

        # Concatenate
        combined = torch.cat([code_emb, graph_emb], dim=1)

        # Learnable gating
        gate_weights = torch.sigmoid(self.gate(combined))

        fused = gate_weights * code_emb + (1 - gate_weights) * graph_emb

        output = self.classifier(fused)

        return output