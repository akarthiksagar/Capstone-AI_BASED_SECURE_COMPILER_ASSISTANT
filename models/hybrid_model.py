import torch
import torch.nn as nn
from models.gnn_encoder import SecureGNN
from models.transformer_encoder import CodeBERTEncoder


class HybridModel(nn.Module):
    """
    Hybrid Vulnerability Detection Model
    ====================================
    
    Combines:
    - GNN (graph structure): Program Dependence Graph analysis
    - CodeBERT (semantics): Code semantic understanding
    - Fusion layer: Joint representation for classification
    """

    def __init__(
        self,
        graph_input_dim=256,
        num_gnn_layers=3,
        gnn_hidden_dim=128,
        gnn_output_dim=128,
        code_embedding_dim=768,
        fusion_hidden_dim=512,
        dropout=0.3
    ):
        super().__init__()

        # GNN Encoder for PDG structures
        self.gnn = SecureGNN(
            input_dim=graph_input_dim,
            hidden_dim=gnn_hidden_dim,
            output_dim=gnn_output_dim,
            num_layers=num_gnn_layers,
            dropout=dropout,
            num_edge_types=2  # DATA_DEP, CONTROL_DEP
        )
        
        # CodeBERT Encoder for semantic understanding
        self.transformer = CodeBERTEncoder(
            model_name="microsoft/codebert-base",
            freeze_layers=8
        )

        # Fusion layer
        fusion_input_dim = gnn_output_dim + code_embedding_dim
        
        self.fusion = nn.Sequential(
            nn.Linear(fusion_input_dim, fusion_hidden_dim),
            nn.BatchNorm1d(fusion_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(fusion_hidden_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 2)  # Binary classification: safe/vulnerable
        )
        
        self.gnn_output_dim = gnn_output_dim
        self.code_embedding_dim = code_embedding_dim

    def forward(self, X, edge_index, edge_types, batch_ids, code_list, device):
        """
        Forward pass through hybrid model.
        
        Args:
            X: Node features [num_nodes, input_dim]
            edge_index: Edge connectivity [2, num_edges]
            edge_types: Edge types [num_edges]
            batch_ids: Graph assignment [num_nodes]
            code_list: List of source code strings
            device: Computation device
        
        Returns:
            logits: Classification logits [batch_size, 2]
        """
        # Graph-level embedding from GNN
        graph_embedding = self.gnn(X, edge_index, edge_types, batch_ids)
        
        # Code-level embedding from CodeBERT
        transformer_embedding = self.transformer(code_list, device)
        
        # Ensure shapes match batch size
        batch_size = len(code_list)
        assert graph_embedding.shape[0] == batch_size, f"Batch size mismatch: {graph_embedding.shape[0]} vs {batch_size}"
        assert transformer_embedding.shape[0] == batch_size, f"Batch size mismatch: {transformer_embedding.shape[0]} vs {batch_size}"
        
        # Fuse representations
        fused = torch.cat([graph_embedding, transformer_embedding], dim=1)
        
        # Classification
        logits = self.fusion(fused)

        return logits