import torch
from transformers import AutoModel, AutoTokenizer


class CodeEncoder(torch.nn.Module):

    def __init__(self, model_name="microsoft/codebert-base"):
        super().__init__()

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def forward(self, code_snippet):

        tokens = self.tokenizer(
            code_snippet,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )

        outputs = self.model(**tokens)

        # CLS token embedding
        cls_embedding = outputs.last_hidden_state[:, 0, :]

        return cls_embedding