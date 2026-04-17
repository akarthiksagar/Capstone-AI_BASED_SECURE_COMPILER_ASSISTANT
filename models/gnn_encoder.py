import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv
from torch_geometric.nn import global_mean_pool, global_add_pool


class EdgeTypeGraphConv(nn.Module):
    """
    Graph convolution layer that respects edge types.
    Applies separate transformations for DATA_DEP and CONTROL_DEP edges.
    """
    def __init__(self, in_channels, out_channels, num_edge_types=2, normalize=True):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_edge_types = num_edge_types
        self.normalize = normalize
        
        # Separate transformations per edge type
        self.W_edge_type = nn.ModuleList([
            nn.Linear(in_channels, out_channels)
            for _ in range(num_edge_types)
        ])
        
        # Self-loop
        self.W_self = nn.Linear(in_channels, out_channels)
        
        # Learnable edge type weights
        self.edge_type_weight = nn.Parameter(torch.ones(num_edge_types))
        
    def forward(self, x, edge_index, edge_types):
        """
        x: node features [num_nodes, in_channels]
        edge_index: edge connectivity [2, num_edges]
        edge_types: edge type ids [num_edges]
        """
        num_nodes = x.size(0)
        out = torch.zeros(num_nodes, self.out_channels, device=x.device)
        
        # Aggregate by edge type
        src_nodes = edge_index[0].long()
        dst_nodes = edge_index[1].long()
        
        for edge_type_id in range(self.num_edge_types):
            mask = (edge_types == edge_type_id)
            if mask.sum() > 0:
                src_masked = src_nodes[mask]
                dst_masked = dst_nodes[mask]
                
                # Get messages from source nodes
                messages = self.W_edge_type[edge_type_id](x[src_masked])
                
                # Aggregate to destination nodes
                out.index_add_(0, dst_masked, messages)
        
        # Add self-loop
        out = out + self.W_self(x)
        
        # Normalize by degree (optional)
        if self.normalize:
            degrees = torch.zeros(num_nodes, device=x.device)
            degrees.index_add_(0, dst_nodes, torch.ones(len(dst_nodes), device=x.device))
            degrees[degrees == 0] = 1  # Avoid division by zero
            out = out / degrees.unsqueeze(1)
        
        return F.relu(out)


class SecureGNN(nn.Module):
    """
    Enhanced GNN encoder for Program Dependence Graphs.
    Handles:
      - Node features (opcode embeddings, security labels)
      - Multiple edge types (DATA_DEP, CONTROL_DEP)
      - Graph-level pooling for classification
      - Attention-based aggregation
    """
    def __init__(
        self,
        input_dim=256,
        hidden_dim=128,
        output_dim=128,
        num_layers=3,
        dropout=0.3,
        num_edge_types=2
    ):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        self.dropout = dropout
        self.num_edge_types = num_edge_types
        
        # Input projection
        self.input_projection = nn.Linear(input_dim, hidden_dim) if input_dim != hidden_dim else nn.Identity()
        
        # Graph convolution layers with edge awareness
        self.layers = nn.ModuleList()
        for i in range(num_layers):
            in_dim = hidden_dim if i > 0 else hidden_dim
            out_dim = hidden_dim if i < num_layers - 1 else output_dim
            
            layer = EdgeTypeGraphConv(in_dim, out_dim, num_edge_types, normalize=True)
            self.layers.append(layer)
        
        # Batch normalization
        self.batch_norms = nn.ModuleList([
            nn.BatchNorm1d(hidden_dim) if i < num_layers - 1 else nn.Identity()
            for i in range(num_layers)
        ])
        
        # Readout (graph-level pooling)
        self.readout_mlp = nn.Sequential(
            nn.Linear(output_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim)
        )
        
    def forward(self, x, edge_index, edge_types, batch_ids=None):
        """
        x: node features [num_nodes, input_dim]
        edge_index: edge connectivity [2, num_edges]
        edge_types: edge type ids [num_edges]
        batch_ids: graph assignment [num_nodes] (for batched graphs)
        """
        # Project input features
        x = self.input_projection(x)
        
        # Graph convolution layers
        for i, (layer, bn) in enumerate(zip(self.layers, self.batch_norms)):
            x = layer(x, edge_index, edge_types)
            x = bn(x) if not isinstance(bn, nn.Identity) else x
            if i < len(self.layers) - 1:
                x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Graph-level pooling
        if batch_ids is not None:
            # For batched graphs
            graph_embedding = global_mean_pool(x, batch_ids)
        else:
            # For single graph - mean pooling over all nodes
            graph_embedding = x.mean(dim=0, keepdim=True)
        
        # Final readout
        graph_embedding = self.readout_mlp(graph_embedding)
        
        return graph_embedding