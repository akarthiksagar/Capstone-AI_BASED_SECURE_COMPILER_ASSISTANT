import torch
from models.graph_dataset import SecureGraphDataset
from models.hybrid_model import HybridModel   # import your model architecture

# Initialize the model architecture
model = HybridModel()

# Load the trained weights
state_dict = torch.load("models/hybrid_model.pt", map_location=torch.device("cpu"))
model.load_state_dict(state_dict)

# Set model to evaluation mode
model.eval()

code = """
x = input()
a = x
b = a
c = b
exec(c)
"""

# Convert code to graph
graph = SecureGraphDataset(code)

with torch.no_grad():
    out = model(graph.x, graph.edge_index, None)

pred = torch.argmax(out, dim=1).item()

if pred == 1:
    print("⚠ Vulnerable Code Detected")
else:
    print("✓ Code is Safe")