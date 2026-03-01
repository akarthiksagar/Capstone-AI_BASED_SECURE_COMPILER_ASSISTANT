import torch
import torch.nn.functional as F
from models.fusion_model import SecureFusionModel


def train_step(model, code_snippet, graph_data, label, optimizer):

    model.train()
    optimizer.zero_grad()

    output = model(code_snippet, graph_data)

    loss = F.cross_entropy(output, label)

    loss.backward()
    optimizer.step()

    return loss.item()