from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

MODEL = "models/codebert-secure"

tokenizer = RobertaTokenizer.from_pretrained(MODEL)
model = RobertaForSequenceClassification.from_pretrained(MODEL)

model.eval()

def predict(code):

    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)

    with torch.no_grad():
        out = model(**inputs)

    prob = torch.softmax(out.logits, dim=1)[0][1].item()

    return prob


# TEST
code = open("sample_programs/test.secure").read()

print("Vulnerability probability:", predict(code))