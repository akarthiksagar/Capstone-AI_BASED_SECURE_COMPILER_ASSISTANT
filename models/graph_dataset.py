import torch
from torch.utils.data import Dataset


# =========================================================
# Dataset Loader
# =========================================================

class SecureGraphDataset(Dataset):

    def __init__(self, file_path):
        self.data = torch.load(file_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]


# =========================================================
# Custom Collate Function (Hybrid Ready)
# =========================================================

def graph_collate_fn(batch):

    X_list = []
    edge_index_list = []
    edge_type_list = []
    labels = []
    code_list = []

    node_offset = 0
    batch_graph_indicator = []
    graph_id = 0

    for sample in batch:

        X = sample["X"]
        edge_index = sample["edge_index"]
        edge_types = sample["edge_types"]
        label = sample["label"]
        code = sample["code"]   # 🔥 NEW

        X_list.append(X)
        code_list.append(code)

        # Offset edge indices for batching
        edge_index_list.append(edge_index + node_offset)
        edge_type_list.append(edge_types)
        labels.append(label)

        # Build graph indicator
        batch_graph_indicator.extend([graph_id] * X.size(0))

        node_offset += X.size(0)
        graph_id += 1

    # Concatenate batched tensors
    X_batch = torch.cat(X_list, dim=0)
    edge_index_batch = torch.cat(edge_index_list, dim=1)
    edge_type_batch = torch.cat(edge_type_list, dim=0)
    labels_batch = torch.stack(labels)
    batch_graph_indicator = torch.tensor(batch_graph_indicator, dtype=torch.long)

    return (
        X_batch,
        edge_index_batch,
        edge_type_batch,
        labels_batch,
        batch_graph_indicator,
        code_list   # 🔥 NEW
    )