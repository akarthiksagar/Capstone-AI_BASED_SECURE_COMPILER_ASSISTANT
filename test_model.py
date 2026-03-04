import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_NAME = "microsoft/codebert-base"
MAX_LEN = 128

# -------------------------------------------------
# MODEL (same as training)
# -------------------------------------------------

class HybridModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.transformer = AutoModel.from_pretrained(MODEL_NAME)

        self.graph_fc = nn.Sequential(
            nn.Linear(7, 32),
            nn.ReLU(),
            nn.Linear(32, 32)
        )

        self.classifier = nn.Sequential(
            nn.Linear(768 + 32, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 2)
        )

    def forward(self, input_ids, attention_mask, graph_feat):

        transformer_out = self.transformer(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        cls_embedding = transformer_out.last_hidden_state[:, 0, :]

        graph_embedding = self.graph_fc(graph_feat)

        combined = torch.cat([cls_embedding, graph_embedding], dim=1)

        return self.classifier(combined)


# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------

model = HybridModel().to(DEVICE)
model.load_state_dict(torch.load("models/hybrid_secure_10k.pt", map_location=DEVICE))
model.eval()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# -------------------------------------------------
# TEST CODE
# -------------------------------------------------

code = """
x = input()
a = x
b = a
c = b
exec(c)
"""

encoding = tokenizer(
    code,
    padding="max_length",
    truncation=True,
    max_length=MAX_LEN,
    return_tensors="pt"
)

graph_feat = torch.tensor([
    code.count("if"),
    code.count("while"),
    code.count("exec"),
    code.count("open_file"),
    code.count("db_query"),
    code.count("="),
    len(code)
], dtype=torch.float).unsqueeze(0)

input_ids = encoding["input_ids"].to(DEVICE)
attention_mask = encoding["attention_mask"].to(DEVICE)
graph_feat = graph_feat.to(DEVICE)

# -------------------------------------------------
# PREDICTION
# -------------------------------------------------

with torch.no_grad():
    output = model(input_ids, attention_mask, graph_feat)

pred = torch.argmax(output, dim=1).item()

if pred == 1:
    print("⚠ Vulnerable Code Detected")
else:
    print("✓ Code is Safe")