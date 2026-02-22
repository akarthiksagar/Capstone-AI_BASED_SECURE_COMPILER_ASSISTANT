from transformers import RobertaTokenizer, RobertaForSequenceClassification
from datasets import Dataset
import torch
from pathlib import Path

MODEL = "microsoft/codebert-base"

tokenizer = RobertaTokenizer.from_pretrained(MODEL)


data = []

root = Path("datasets/converted/train")

for f in root.glob("*.secure"):

    code = f.read_text(errors="ignore")

    label = 1 if "vulnerable" in f.name else 0

    data.append({"code": code, "label": label})

dataset = Dataset.from_list(data)



def tokenize(x):
    return tokenizer(
        x["code"],
        truncation=True,
        padding="max_length",
        max_length=512
    )

dataset = dataset.map(tokenize)

dataset.set_format(type="torch", columns=["input_ids","attention_mask","label"])



model = RobertaForSequenceClassification.from_pretrained(MODEL, num_labels=2)


optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)

model.train()

for epoch in range(2):

    for batch in dataset:

        outputs = model(
            input_ids=batch["input_ids"].unsqueeze(0),
            attention_mask=batch["attention_mask"].unsqueeze(0),
            labels=batch["label"].unsqueeze(0)
        )

        loss = outputs.loss

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    print("Epoch done")

model.save_pretrained("models/codebert-secure")
print("TRAINING COMPLETE")