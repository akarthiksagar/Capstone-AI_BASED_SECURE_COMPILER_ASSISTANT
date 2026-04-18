import torch
import os
from torch.utils.data import Dataset


class SecureGraphDataset(Dataset):
    """
    Dataset loader for pre-compiled PDG graphs.
    
    Expected format: list of dicts with keys:
      - X: node features [num_nodes, input_dim]
      - edge_index: [2, num_edges]
      - edge_types: [num_edges]
      - label: int (0 or 1)
      - code: str (source code)
    """

    def __init__(self, data):
        """
        Args:
            data: Either file path (str) or list of sample dicts
        """
        if isinstance(data, str):
            self.data = torch.load(data)
        else:
            self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


def graph_collate_fn(batch):
    """
    Custom collate function for batching graph data.
    
    Returns dict with batched tensors and raw code list.
    """
    X_list = []
    edge_index_list = []
    edge_type_list = []
    labels = []
    code_list = []
    
    node_offset = 0
    batch_graph_indicator = []
    graph_id = 0
    
    for sample in batch:
        X = sample.get("X", sample[0]) if isinstance(sample, (list, tuple)) else sample["X"]
        edge_index = sample.get("edge_index", sample[1]) if isinstance(sample, (list, tuple)) else sample["edge_index"]
        edge_types = sample.get("edge_types", sample[2]) if isinstance(sample, (list, tuple)) else sample["edge_types"]
        label = sample.get("label", sample[3]) if isinstance(sample, (list, tuple)) else sample["label"]
        code = sample.get("code", "") if isinstance(sample, (list, tuple)) else sample.get("code", "")
        
        # Ensure tensors
        if not isinstance(X, torch.Tensor):
            X = torch.tensor(X, dtype=torch.float)
        else:
            X = X.float()

        # Normalize node feature width across samples.
        # Default target is 256 to match model_config graph_input_dim.
        target_dim = int(os.getenv("GRAPH_INPUT_DIM", "256"))
        if X.dim() == 1:
            X = X.unsqueeze(0)
        feature_dim = X.size(1)
        if feature_dim < target_dim:
            pad = torch.zeros((X.size(0), target_dim - feature_dim), dtype=X.dtype)
            X = torch.cat([X, pad], dim=1)
        elif feature_dim > target_dim:
            X = X[:, :target_dim]

        if not isinstance(edge_index, torch.Tensor):
            edge_index = torch.tensor(edge_index, dtype=torch.long)
        if not isinstance(edge_types, torch.Tensor):
            edge_types = torch.tensor(edge_types, dtype=torch.long)
        if not isinstance(label, torch.Tensor):
            label = torch.tensor(label, dtype=torch.long)
        
        X_list.append(X)
        code_list.append(code)
        
        # Offset edge indices for batching
        if edge_index.numel() > 0:
            edge_index_list.append(edge_index + node_offset)
        else:
            edge_index_list.append(torch.zeros((2, 0), dtype=torch.long))
        
        edge_type_list.append(edge_types)
        labels.append(label)
        
        # Build graph indicator (which graph each node belongs to)
        batch_graph_indicator.extend([graph_id] * X.size(0))
        
        node_offset += X.size(0)
        graph_id += 1
    
    # Concatenate batched tensors
    X_batch = torch.cat(X_list, dim=0)
    edge_index_batch = torch.cat(edge_index_list, dim=1) if edge_index_list else torch.zeros((2, 0), dtype=torch.long)
    edge_type_batch = torch.cat(edge_type_list, dim=0) if edge_type_list else torch.zeros((0,), dtype=torch.long)
    labels_batch = torch.stack(labels)
    batch_graph_indicator = torch.tensor(batch_graph_indicator, dtype=torch.long)
    
    return {
        'X': X_batch,
        'edge_index': edge_index_batch,
        'edge_types': edge_type_batch,
        'batch_ids': batch_graph_indicator,
        'label': labels_batch,
        'code_list': code_list
    }
