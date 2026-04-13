# # # from torch.utils.data import DataLoader
# # # from models.graph_dataset import SecureGraphDataset, graph_collate_fn

# # # dataset = SecureGraphDataset("dataset/graph_dataset.pt")

# # # loader = DataLoader(
# # #     dataset,
# # #     batch_size=4,
# # #     shuffle=True,
# # #     collate_fn=graph_collate_fn
# # # )

# # # for X, edge_index, edge_types, labels in loader:
# # #     print("X:", X.shape)
# # #     print("edge_index:", edge_index.shape)
# # #     print("edge_types:", edge_types.shape)
# # #     print("labels:", labels.shape)
# # #     break


# # # import torch
# # # from torch.utils.data import DataLoader

# # # from models.graph_dataset import SecureGraphDataset, graph_collate_fn
# # # from models.gnn_encoder import SecureGNN


# # # # 1️⃣ Load Dataset
# # # dataset = SecureGraphDataset("dataset/graph_dataset.pt")

# # # loader = DataLoader(
# # #     dataset,
# # #     batch_size=4,
# # #     shuffle=True,
# # #     collate_fn=graph_collate_fn
# # # )


# # # # 2️⃣ Initialize Model
# # # input_dim = dataset[0]["X"].shape[1]
# # # model = SecureGNN(input_dim=input_dim)

# # # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# # # model = model.to(device)


# # # # 3️⃣ Test Forward Pass
# # # for X, edge_index, edge_types, labels, batch_ids in loader:

# # #     X = X.to(device)
# # #     edge_index = edge_index.to(device)
# # #     edge_types = edge_types.to(device)
# # #     batch_ids = batch_ids.to(device)

# # #     logits = model(X, edge_index, edge_types, batch_ids)

# # #     print("Logits shape:", logits.shape)
# # #     break


# # # import torch
# # # import torch.nn as nn
# # # from torch.utils.data import DataLoader
# # # from sklearn.model_selection import train_test_split

# # # from models.graph_dataset import SecureGraphDataset, graph_collate_fn
# # # from models.gnn_encoder import SecureGNN


# # # # ==========================================================
# # # # Load Dataset
# # # # ==========================================================

# # # dataset = SecureGraphDataset("dataset/graph_dataset.pt")

# # # train_indices, val_indices = train_test_split(
# # #     list(range(len(dataset))),
# # #     test_size=0.2,
# # #     random_state=42,
# # #     stratify=[dataset[i]["label"].item() for i in range(len(dataset))]
# # # )

# # # train_subset = torch.utils.data.Subset(dataset, train_indices)
# # # val_subset = torch.utils.data.Subset(dataset, val_indices)

# # # train_loader = DataLoader(
# # #     train_subset,
# # #     batch_size=16,
# # #     shuffle=True,
# # #     collate_fn=graph_collate_fn
# # # )

# # # val_loader = DataLoader(
# # #     val_subset,
# # #     batch_size=16,
# # #     shuffle=False,
# # #     collate_fn=graph_collate_fn
# # # )


# # # # ==========================================================
# # # # Model Setup
# # # # ==========================================================

# # # input_dim = dataset[0]["X"].shape[1]
# # # model = SecureGNN(input_dim=input_dim, hidden_dim=64, num_layers=3)

# # # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# # # model = model.to(device)

# # # criterion = nn.CrossEntropyLoss()
# # # optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)


# # # # ==========================================================
# # # # Training Loop
# # # # ==========================================================

# # # def train_one_epoch():
# # #     model.train()
# # #     total_loss = 0
# # #     correct = 0
# # #     total = 0

# # #     for X, edge_index, edge_types, labels, batch_ids in train_loader:

# # #         X = X.to(device)
# # #         edge_index = edge_index.to(device)
# # #         edge_types = edge_types.to(device)
# # #         labels = labels.to(device)
# # #         batch_ids = batch_ids.to(device)

# # #         optimizer.zero_grad()

# # #         logits = model(X, edge_index, edge_types, batch_ids)
# # #         loss = criterion(logits, labels)

# # #         loss.backward()
# # #         optimizer.step()

# # #         total_loss += loss.item()
# # #         preds = torch.argmax(logits, dim=1)
# # #         correct += (preds == labels).sum().item()
# # #         total += labels.size(0)

# # #     return total_loss / len(train_loader), correct / total


# # # def evaluate():
# # #     model.eval()
# # #     correct = 0
# # #     total = 0

# # #     with torch.no_grad():
# # #         for X, edge_index, edge_types, labels, batch_ids in val_loader:

# # #             X = X.to(device)
# # #             edge_index = edge_index.to(device)
# # #             edge_types = edge_types.to(device)
# # #             labels = labels.to(device)
# # #             batch_ids = batch_ids.to(device)

# # #             logits = model(X, edge_index, edge_types, batch_ids)
# # #             preds = torch.argmax(logits, dim=1)

# # #             correct += (preds == labels).sum().item()
# # #             total += labels.size(0)

# # #     return correct / total


# # # # ==========================================================
# # # # Run Training
# # # # ==========================================================

# # # epochs = 10

# # # for epoch in range(epochs):

# # #     train_loss, train_acc = train_one_epoch()
# # #     val_acc = evaluate()

# # #     print(f"Epoch {epoch+1}")
# # #     print(f"Train Loss: {train_loss:.4f}")
# # #     print(f"Train Acc : {train_acc:.4f}")
# # #     print(f"Val Acc   : {val_acc:.4f}")
# # #     print("-" * 40)

# # import torch
# # from torch.utils.data import DataLoader, Subset
# # from sklearn.model_selection import train_test_split
# # from sklearn.metrics import classification_report

# # from models.graph_dataset import SecureGraphDataset, graph_collate_fn
# # from models.hybrid_model import HybridModel


# # # =========================================================
# # # Device
# # # =========================================================

# # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# # print("Using device:", device)


# # # =========================================================
# # # Load Dataset
# # # =========================================================

# # dataset = SecureGraphDataset("dataset/graph_dataset.pt")

# # sample = dataset[0]
# # graph_input_dim = sample["X"].size(1)


# # # =========================================================
# # # Train / Validation Split
# # # =========================================================

# # indices = list(range(len(dataset)))
# # train_idx, val_idx = train_test_split(
# #     indices,
# #     test_size=0.2,
# #     random_state=42,
# #     stratify=[dataset[i]["label"].item() for i in indices]
# # )

# # train_subset = Subset(dataset, train_idx)
# # val_subset = Subset(dataset, val_idx)

# # train_loader = DataLoader(
# #     train_subset,
# #     batch_size=4,
# #     shuffle=True,
# #     collate_fn=graph_collate_fn
# # )

# # val_loader = DataLoader(
# #     val_subset,
# #     batch_size=4,
# #     shuffle=False,
# #     collate_fn=graph_collate_fn
# # )


# # # =========================================================
# # # Model
# # # =========================================================

# # model = HybridModel(graph_input_dim).to(device)
# # optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
# # criterion = torch.nn.CrossEntropyLoss()


# # # =========================================================
# # # Training Loop
# # # =========================================================

# # # num_epochs = 10

# # # for epoch in range(num_epochs):

# # #     # -------------------------
# # #     # TRAIN
# # #     # -------------------------
# # #     model.train()
# # #     train_correct = 0
# # #     train_total = 0
# # #     train_loss_total = 0

# # #     for X, edge_index, edge_types, labels, batch_ids, code_list in train_loader:

# # #         X = X.to(device)
# # #         edge_index = edge_index.to(device)
# # #         edge_types = edge_types.to(device)
# # #         labels = labels.to(device)
# # #         batch_ids = batch_ids.to(device)

# # #         logits = model(
# # #             X,
# # #             edge_index,
# # #             edge_types,
# # #             batch_ids,
# # #             code_list,
# # #             device
# # #         )

# # #         loss = criterion(logits, labels)

# # #         optimizer.zero_grad()
# # #         loss.backward()
# # #         optimizer.step()

# # #         train_loss_total += loss.item()

# # #         preds = torch.argmax(logits, dim=1)
# # #         train_correct += (preds == labels).sum().item()
# # #         train_total += labels.size(0)

# # #     train_accuracy = train_correct / train_total


# # #     # -------------------------
# # #     # VALIDATION
# # #     # -------------------------
# # #     model.eval()
# # #     val_correct = 0
# # #     val_total = 0
# # #     all_preds = []
# # #     all_labels = []

# # #     with torch.no_grad():
# # #         for X, edge_index, edge_types, labels, batch_ids, code_list in val_loader:

# # #             X = X.to(device)
# # #             edge_index = edge_index.to(device)
# # #             edge_types = edge_types.to(device)
# # #             labels = labels.to(device)
# # #             batch_ids = batch_ids.to(device)

# # #             logits = model(
# # #                 X,
# # #                 edge_index,
# # #                 edge_types,
# # #                 batch_ids,
# # #                 code_list,
# # #                 device
# # #             )

# # #             preds = torch.argmax(logits, dim=1)

# # #             val_correct += (preds == labels).sum().item()
# # #             val_total += labels.size(0)

# # #             all_preds.extend(preds.cpu().numpy())
# # #             all_labels.extend(labels.cpu().numpy())

# # #     val_accuracy = val_correct / val_total

# # #     print(f"\nEpoch {epoch+1}")
# # #     print(f"Train Accuracy: {train_accuracy:.4f}")
# # #     print(f"Validation Accuracy: {val_accuracy:.4f}")


# # # =========================================================
# # # Final Evaluation Report
# # # =========================================================

# # # print("\nClassification Report (Validation Set):")
# # # print(classification_report(all_labels, all_preds))


# # codes = [dataset[i]["code"] for i in range(len(dataset))]
# # labels = [dataset[i]["label"].item() for i in range(len(dataset))]

# # vuln = sum(labels)
# # safe = len(labels) - vuln

# # print("Vulnerable:", vuln)
# # print("Safe:", safe)

# # # Count unique codes
# # print("Unique codes:", len(set(codes)))


# import torch
# import torch.nn as nn
# from torch.utils.data import DataLoader, random_split
# import os

# from models.graph_dataset import SecureGraphDataset, graph_collate_fn
# from models.hybrid_model import HybridModel


# # ============================================================
# # DEVICE
# # ============================================================

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("Using device:", device)


# # ============================================================
# # LOAD GRAPH DATASET
# # ============================================================

# dataset_path = "dataset/graph_dataset.pt"

# if not os.path.exists(dataset_path):
#     raise FileNotFoundError("Graph dataset not found. Generate it first.")

# dataset = SecureGraphDataset(dataset_path)

# print("Total samples:", len(dataset))

# sample = dataset[0]
# graph_input_dim = sample["X"].size(1)

# print("Graph feature dimension:", graph_input_dim)


# # ============================================================
# # TRAIN / VALIDATION SPLIT
# # ============================================================

# train_size = int(0.8 * len(dataset))
# val_size = len(dataset) - train_size

# train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# print("Train size:", len(train_dataset))
# print("Val size:", len(val_dataset))


# train_loader = DataLoader(
#     train_dataset,
#     batch_size=16,
#     shuffle=True,
#     collate_fn=graph_collate_fn
# )

# val_loader = DataLoader(
#     val_dataset,
#     batch_size=16,
#     shuffle=False,
#     collate_fn=graph_collate_fn
# )


# # ============================================================
# # MODEL
# # ============================================================

# model = HybridModel(graph_input_dim).to(device)

# optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
# criterion = nn.CrossEntropyLoss()

# print("Model initialized.")
# print("Total parameters:",
#       sum(p.numel() for p in model.parameters()))


# # ============================================================
# # TRAINING LOOP
# # ============================================================

# epochs = 10

# for epoch in range(epochs):

#     # ---------------- TRAIN ----------------
#     model.train()
#     total_correct = 0
#     total = 0
#     total_loss = 0

#     for X, edge_index, edge_types, labels, batch_ids, code_list in train_loader:

#         X = X.to(device)
#         edge_index = edge_index.to(device)
#         edge_types = edge_types.to(device)
#         labels = labels.to(device)
#         batch_ids = batch_ids.to(device)

#         logits = model(
#             X,
#             edge_index,
#             edge_types,
#             batch_ids,
#             code_list,
#             device
#         )

#         loss = criterion(logits, labels)

#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()

#         total_loss += loss.item()

#         preds = torch.argmax(logits, dim=1)
#         total_correct += (preds == labels).sum().item()
#         total += labels.size(0)

#     train_acc = total_correct / total

#     # ---------------- VALIDATION ----------------
#     model.eval()
#     val_correct = 0
#     val_total = 0

#     with torch.no_grad():
#         for X, edge_index, edge_types, labels, batch_ids, code_list in val_loader:

#             X = X.to(device)
#             edge_index = edge_index.to(device)
#             edge_types = edge_types.to(device)
#             labels = labels.to(device)
#             batch_ids = batch_ids.to(device)

#             logits = model(
#                 X,
#                 edge_index,
#                 edge_types,
#                 batch_ids,
#                 code_list,
#                 device
#             )

#             preds = torch.argmax(logits, dim=1)
#             val_correct += (preds == labels).sum().item()
#             val_total += labels.size(0)

#     val_acc = val_correct / val_total

#     print(f"Epoch {epoch+1}/{epochs}")
#     print(f"  Train Loss: {total_loss:.4f}")
#     print(f"  Train Acc : {train_acc:.4f}")
#     print(f"  Val Acc   : {val_acc:.4f}")
#     print("-" * 40)


# # ============================================================
# # FINAL SUMMARY
# # ============================================================

# print("\nTraining Complete.")


import torch
from torch.utils.data import DataLoader

# ==============================
# Compiler Pipeline Imports
# ==============================
from frontend.parser_driver import parse_source
from frontend.ast_builder import ASTBuilder
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from analysis.graph_tensorizer import GraphTensorizer

# ==============================
# ML Imports
# ==============================
from models.graph_dataset import SecureGraphDataset, graph_collate_fn
from models.hybrid_model import HybridModel
from pipeline.compiler_pipeline import SecureCompilerPipeline
from frontend.parser_driver import parse_source
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from analysis.graph_tensorizer import GraphTensorizer

code = """
x = input()
a = x
b = a
c = b
exec(c)
"""


print("====== SOURCE ======")
print(code)


# 1️⃣ Parse
print("\n====== PARSING ======")
ast = parse_source(code)
print("AST built successfully")

print("\n====== AST STRUCTURE ======")
print(ast)

def print_ast(node, indent=0):
    print(" " * indent + node.__class__.__name__)
    for attr in vars(node).values():
        if isinstance(attr, list):
            for item in attr:
                if hasattr(item, "__class__"):
                    print_ast(item, indent + 2)
        elif hasattr(attr, "__class__") and hasattr(attr, "accept"):
            print_ast(attr, indent + 2)

print_ast(ast)

# 2️⃣ Semantic
print("\n====== SEMANTIC ANALYSIS ======")
semantic = SemanticAnalyzer()
ast.accept(semantic)

if semantic.errors:
    print("Semantic Errors:")
    for e in semantic.errors:
        print(e)
    exit()
print("Semantic analysis complete")
# 3️⃣ IR Generation
print("\n====== IR GENERATION ======")
ir_builder = IRBuilder()
cfg = ast.accept(ir_builder)

for block in cfg.blocks:
    print(f"\nBlock: {block.name}")
    for instr in block.instructions:
        print("   ", instr)


# 4️⃣ SSA Transform
print("\n====== SSA TRANSFORMATION ======")
ssa = SSATransformer(cfg)
cfg = ssa.transform()

for block in cfg.blocks:
    print(f"\nBlock: {block.name}")
    for instr in block.instructions:
        print("   ", instr)


# 5️⃣ PDG Build
print("\n====== PDG BUILD ======")
pdg_builder = PDGBuilder(cfg)
pdg = pdg_builder.build()

print(f"\nPDG Nodes: {len(pdg.nodes)}")
print(f"PDG Edges: {len(pdg.edges)}")

for edge in pdg.edges:
    print(f"{edge.source} --{edge.type}--> {edge.target}")


tensorizer = GraphTensorizer()
X,edge_index,edge_types=tensorizer.tensorize(pdg)

print("\n====== GRAPH TENSORS ======")
print("Node Feature Matrix Shape:", X.shape)
print("Edge Index Shape:", edge_index.shape)
print("Edge Types Shape:", edge_types.shape)

# ==========================================================
# 2️⃣ Dataset + Model Training Demo
# ==========================================================

print("\n==============================")
print("🧠 AI TRAINING PIPELINE")
print("==============================\n")

dataset = SecureGraphDataset("dataset/graph_dataset.pt")

print("Total dataset samples:", len(dataset))

sample = dataset[0]
graph_input_dim = sample["X"].size(1)

loader = DataLoader(
    dataset,
    batch_size=16,
    shuffle=True,
    collate_fn=graph_collate_fn
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)
model = HybridModel(graph_input_dim).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
criterion = torch.nn.CrossEntropyLoss()

# Train for 1 epoch (demo purpose)
model.train()
total_correct = 0
total = 0

for X, edge_index, edge_types, labels, batch_ids, code_list in loader:

    X = X.to(device)
    edge_index = edge_index.to(device)
    edge_types = edge_types.to(device)
    labels = labels.to(device)
    batch_ids = batch_ids.to(device)

    logits = model(
        X,
        edge_index,
        edge_types,
        batch_ids,
        code_list,
        device
    )

    loss = criterion(logits, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    preds = torch.argmax(logits, dim=1)
    total_correct += (preds == labels).sum().item()
    total += labels.size(0)

accuracy = total_correct / total

print("\nTraining Accuracy (1 epoch demo):", round(accuracy, 4))