import torch
from torch.optim import Adam
from torch.utils.data import DataLoader

from dataset.juliet_dataset import JulietDataset
from pipeline.compiler_pipeline import SecureCompilerPipeline
from models.fusion_model import SecureFusionModel


def train():

    dataset = JulietDataset("data/juliet")
    pipeline = SecureCompilerPipeline()
    model = SecureFusionModel()

    optimizer = Adam(model.parameters(), lr=1e-4)

    for epoch in range(5):

        total_loss = 0

        for code, label in dataset:

            graph, errors = pipeline.compile_to_pdg(code)

            if errors:
                continue

            label_tensor = torch.tensor([label])

            optimizer.zero_grad()

            output = model([code], graph)

            loss = torch.nn.functional.cross_entropy(output, label_tensor)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch}, Loss: {total_loss}")