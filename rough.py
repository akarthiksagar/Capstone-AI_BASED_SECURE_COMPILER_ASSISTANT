#For removing duplicate entries
# import json
# import hashlib

# INPUT = "dataset/juliet_processed.json"
# OUTPUT = "dataset/juliet_processed_dedup.json"

# with open(INPUT, "r") as f:
#     data = json.load(f)

# seen = set()
# dedup = []

# for sample in data:
#     code = sample["code"].strip()
#     h = hashlib.md5(code.encode()).hexdigest()

#     if h not in seen:
#         seen.add(h)
#         dedup.append(sample)

# print("Original:", len(data))
# print("After dedup:", len(dedup))

# with open(OUTPUT, "w") as f:
#     json.dump(dedup, f, indent=2)

# print("Saved deduplicated dataset.")





#for checking the count of good and bad entries
# from collections import Counter
# import json

# with open("dataset/juliet_processed_dedup.json") as f:
#     data = json.load(f)

# labels = Counter([x["label"] for x in data])
# print(labels)



#for balancing the dataset

# import json
# import random

# INPUT = "dataset/juliet_processed_dedup.json"
# OUTPUT = "dataset/juliet_balanced.json"

# with open(INPUT, "r") as f:
#     data = json.load(f)

# safe = [x for x in data if x["label"] == 0]
# vuln = [x for x in data if x["label"] == 1]

# print("Before balancing:")
# print("Safe:", len(safe))
# print("Vulnerable:", len(vuln))

# # Downsample safe
# safe = random.sample(safe, len(vuln))

# balanced = safe + vuln
# random.shuffle(balanced)

# print("After balancing:", len(balanced))

# with open(OUTPUT, "w") as f:
#     json.dump(balanced, f, indent=2)

# print("Saved balanced dataset.")



#for splitting the dataset (train/test)
# from sklearn.model_selection import train_test_split
# import json

# with open("dataset/juliet_balanced.json") as f:
#     data = json.load(f)

# train, val = train_test_split(
#     data,
#     test_size=0.2,
#     random_state=42,
#     stratify=[x["label"] for x in data]
# )

# print("Train:", len(train))
# print("Val:", len(val))
import json
data = json.load(open("dataset/secure_synthetic_10k.json"))
print("Total:", len(data))
print("Vulnerable:", sum(x["label"] for x in data))