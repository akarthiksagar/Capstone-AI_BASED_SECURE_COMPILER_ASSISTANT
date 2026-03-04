import torch
from models.graph_dataset import SecureGraphDataset

model = torch.load("models/hybrid_model.pt")
model.eval()

code = """
x = input()
a = x
b = a
c = b
exec(c)
"""

graph = SecureGraphDataset(code)

with torch.no_grad():
    out = model(graph.x, graph.edge_index, None)

pred = torch.argmax(out, dim=1)

if pred == 1:
    print("⚠ Vulnerable Code Detected")
else:
    print("✓ Code is Safe")