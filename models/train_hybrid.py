import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# =====================================================
# CONFIG
# =====================================================

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 16
EPOCHS = 5
MAX_LEN = 128
MODEL_NAME = "microsoft/codebert-base"

print("Using device:", DEVICE)

# =====================================================
# LOAD DATA
# =====================================================

with open("dataset/secure_synthetic_10k.json") as f:
    data = json.load(f)

train_data, val_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42,
    stratify=[x["label"] for x in data]
)

print("Train size:", len(train_data))
print("Val size:", len(val_data))

# =====================================================
# DATASET
# =====================================================

class SecureDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def simple_graph_features(self, code):
        """
        Lightweight structural features
        (acts as mini-graph embedding)
        """
        return torch.tensor([
            code.count("if"),
            code.count("while"),
            code.count("exec"),
            code.count("open_file"),
            code.count("db_query"),
            code.count("="),
            len(code)
        ], dtype=torch.float)

    def __getitem__(self, idx):
        item = self.data[idx]
        code = item["code"]
        label = torch.tensor(item["label"], dtype=torch.long)

        encoding = self.tokenizer(
            code,
            padding="max_length",
            truncation=True,
            max_length=MAX_LEN,
            return_tensors="pt"
        )

        graph_feat = self.simple_graph_features(code)

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "graph_feat": graph_feat,
            "label": label
        }

# =====================================================
# MODEL
# =====================================================

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

# =====================================================
# TRAIN
# =====================================================

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

train_dataset = SecureDataset(train_data, tokenizer)
val_dataset = SecureDataset(val_data, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

model = HybridModel().to(DEVICE)
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
criterion = nn.CrossEntropyLoss()

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for batch in tqdm(train_loader):
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        graph_feat = batch["graph_feat"].to(DEVICE)
        labels = batch["label"].to(DEVICE)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask, graph_feat)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"\nEpoch {epoch+1} Loss: {total_loss/len(train_loader):.4f}")

    # Validation
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            graph_feat = batch["graph_feat"].to(DEVICE)
            labels = batch["label"].to(DEVICE)

            outputs = model(input_ids, attention_mask, graph_feat)
            preds = torch.argmax(outputs, dim=1)

            correct += (preds == labels).sum().item()
            total += labels.size(0)

    acc = correct / total
    print(f"Validation Accuracy: {acc:.4f}")

# =====================================================
# SAVE MODEL
# =====================================================

torch.save(model.state_dict(), "models/hybrid_secure_10k.pt")
print("Model saved successfully.")