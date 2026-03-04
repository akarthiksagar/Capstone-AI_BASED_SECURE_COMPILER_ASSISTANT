import torch
from models.hybrid_model import HybridModel
from models.graph_dataset import SecureGraphDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load dataset
dataset = SecureGraphDataset("dataset/graph_dataset.pt")

sample = dataset[0]
graph_input_dim = sample["X"].size(1)

# Create model architecture
model = HybridModel(graph_input_dim).to(device)

# Load trained weights
model.load_state_dict(torch.load("models/hybrid_model.pt", map_location=device))

model.eval()

print("Model loaded successfully!")