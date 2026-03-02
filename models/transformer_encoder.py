import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer


class CodeBERTEncoder(nn.Module):

    def __init__(self, model_name="microsoft/codebert-base", freeze_layers=10):
        super().__init__()

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        # Freeze lower layers
        for name, param in self.model.named_parameters():
            if "encoder.layer." in name:
                layer_num = int(name.split("encoder.layer.")[1].split(".")[0])
                if layer_num < freeze_layers:
                    param.requires_grad = False

        self.hidden_size = self.model.config.hidden_size

    def forward(self, code_list, device):

        tokens = self.tokenizer(
            code_list,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt"
        )

        tokens = {k: v.to(device) for k, v in tokens.items()}

        outputs = self.model(**tokens)

        # CLS token embedding
        cls_embedding = outputs.last_hidden_state[:, 0, :]

        return cls_embedding