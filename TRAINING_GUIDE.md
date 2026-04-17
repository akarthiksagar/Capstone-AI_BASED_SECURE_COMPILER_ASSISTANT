# Unified Training & Inference Pipeline

## Complete Guide to Model Training & Deployment

---

## 📋 Overview

This guide explains how to train and deploy the hybrid GNN + CodeBERT vulnerability detection model.

**Architecture:**

```
PDG Graphs → GNN (structure) → 🔗 Fusion Layer → Classification
Code Strings → CodeBERT (semantics) ↗
```

---

## 🎯 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install torch torchvision torchaudio -i https://download.pytorch.org/whl/torch_stable.html
pip install transformers torch_geometric torch_scatter
pip install scikit-learn matplotlib seaborn tqdm
```

### Train in 3 Steps

```bash
# Step 1: Build dataset (compile code → PDG graphs)
python dataset/build_graph_dataset.py

# Step 2: Train model
python train_model.py --config model_config.json

# Step 3: Evaluate
python evaluate_model.py --checkpoint models/secure_gnn_best.pt
```

---

## 📊 Configuration

### `model_config.json` - Central Configuration

All hyperparameters in one place:

```json
{
  "model": {
    "graph_input_dim": 256, // PDG node feature dimension
    "gnn_hidden_dim": 128, // Graph processing hidden layer
    "code_embedding_dim": 768 // CodeBERT output dimension
  },
  "training": {
    "batch_size": 16,
    "epochs": 50,
    "learning_rate": 2e-5,
    "early_stopping_patience": 5 // Stop if no improvement for 5 epochs
  },
  "gnn": {
    "num_layers": 3, // GNN depth
    "edge_types": ["DATA_DEP", "CONTROL_DEP"]
  }
}
```

**Key Settings for Best Results:**

- Increase `gnn_hidden_dim` (128→256) for larger models
- Decrease `learning_rate` (2e-5→1e-5) if training is unstable
- Increase `epochs` (50→100) for more training
- Adjust `batch_size` (16→32) based on GPU memory

---

## 🚀 Training Pipeline

### Step 1: Prepare Dataset

```bash
# Compile code samples → PDG graphs (stored in graph_dataset.pt)
python dataset/build_graph_dataset.py
```

This:

1. Loads `secure_synthetic_10k.json` or Juliet dataset
2. Parses each code snippet using SecureLang compiler
3. Builds Program Dependence Graph (data + control dependencies)
4. Tensorizes to PyTorch graph tensors
5. Splits into train (70%) / val (15%) / test (15%)
6. Saves to `dataset/train_graphs.pt`, `val_graphs.pt`, `test_graphs.pt`

**Quality Check:**

```bash
python -c "
import torch
data = torch.load('dataset/train_graphs.pt')
print(f'Samples: {len(data)}')
print(f'Label distribution: {[s[\"label\"] for s in data[:10]]}')"
```

### Step 2: Train Model

```bash
# Start training
python train_model.py --config model_config.json

# Optional: specify device
python train_model.py --config model_config.json --device cuda:0

# Optional: resume from checkpoint (coming soon)
```

**What happens:**

1. Loads train/val splits
2. Initializes HybridModel with GNN + CodeBERT
3. Trains with:
   - AdamW optimizer with cosine annealing
   - CrossEntropyLoss
   - Early stopping (monitor F1-score)
   - Checkpointing (save best model)
4. Logs metrics to `training.log`

**Expected Training Time:**

- Small dataset (1K samples): ~5-10 minutes on GPU
- Large dataset (10K+ samples): ~30-60 minutes on GPU

**Output Files:**

- `models/secure_gnn_best.pt` - Best model checkpoint
- `models/checkpoints/` - All epoch checkpoints
- `logs/training.log` - Full training log

### Step 3: Monitor Training

Watch metrics in real-time:

```bash
# Linux/Mac
tail -f training.log

# Windows
Get-Content training.log -Wait
```

**Key Metrics:**

- **Loss**: Should decrease over time (target: <0.3)
- **Accuracy**: Target >85% on validation set
- **F1-Score**: Target >0.80 for vulnerability detection
- **Early Stopping**: Triggers if F1 plateaus for 5 epochs

---

## 🆕 New Multi-Source Dataset Pipeline

### Overview

The new pipeline collects code from multiple real-world sources, translates any language to SecureLang, and builds comprehensive vulnerability datasets.

**Key Features:**

- ✅ Multi-source collection (GitHub, CVE databases, OWASP)
- ✅ Universal language translation (Python, C/C++, JavaScript)
- ✅ Enhanced SecureLang grammar for security analysis
- ✅ Automatic vulnerability labeling
- ✅ Real-world code patterns

### Step 1: Collect Multi-Source Data

```bash
# Collect from multiple sources
python dataset/multi_source_collector.py --github-token YOUR_TOKEN --output dataset/multi_source_dataset.json
```

**Sources Included:**

- **GitHub**: Search vulnerable code repositories
- **CVE Database**: Real vulnerability descriptions from NVD
- **OWASP**: Standard vulnerability examples
- **Custom**: Add your own sources

### Step 2: Translate & Build Dataset

```bash
# Translate all languages to SecureLang and build graphs
python dataset/build_multi_source_dataset.py --input dataset/multi_source_dataset.json --output dataset/multi_source_graph_dataset.pt
```

**What happens:**

1. Loads collected code samples
2. Translates each to SecureLang using universal translator
3. Compiles to PDG graphs
4. Labels vulnerabilities automatically
5. Splits into train/val/test sets

### Step 3: Train on Multi-Source Data

```bash
# Use the new dataset
python train_model.py --config model_config.json --dataset dataset/train_graphs.pt
```

### Enhanced SecureLang Grammar

**New Security Constructs:**

- Exception handling: `try/except/finally`
- Context managers: `with` statements
- Assertions: `assert` statements
- Security sinks: `exec`, `eval`, `system`, `sql`, `open`, `connect`, `deserialize`
- Security sources: `input`, `getenv`, `request`

**Example SecureLang Code:**

```securelang
def vulnerable_web_handler(request_data) {
    user_input = request("POST", "user_input")
    // SQL injection vulnerability
    query = sql("SELECT * FROM users WHERE id = " + user_input)
    return query
}

def safe_web_handler(request_data) {
    user_input = request("POST", "user_input")
    // Safe: parameterized query
    query = sql("SELECT * FROM users WHERE id = ?", user_input)
    return query
}
```

### Dataset Statistics

After building, check `dataset/dataset_stats.json`:

```json
{
  "total_samples": 2500,
  "vulnerable": 1250,
  "safe": 1250,
  "sources": {
    "github": 1500,
    "cve": 500,
    "owasp": 500
  },
  "languages": {
    "python": 1200,
    "c": 800,
    "javascript": 500
  }
}
```

### Benefits

- **Real-World Relevance**: Code from actual projects and vulnerabilities
- **Diverse Patterns**: Multiple languages and coding styles
- **Scalable**: Easy to add new sources
- **Accurate Translation**: Maintains security semantics during conversion

### Custom Evaluation

```python
from models.hybrid_model import HybridModel
from models.graph_dataset import SecureGraphDataset, graph_collate_fn
import torch

# Load model
checkpoint = torch.load('models/secure_gnn_best.pt')
model = HybridModel(...)
model.load_state_dict(checkpoint['model_state'])

# Evaluate on custom dataset
test_data = torch.load('dataset/test_graphs.pt')
dataset = SecureGraphDataset(test_data)

for sample in dataset:
    X = sample['X']
    # ... your evaluation code
```

---

## 🔍 Production Inference

### Python API

```python
from inference_production import SecureAnalyzer

# Initialize
analyzer = SecureAnalyzer(
    model_path='models/secure_gnn_best.pt',
    device='cuda'
)

# Analyze single code snippet
code = """
x = input()
exec(x)  # VULNERABLE
"""

result = analyzer.analyze(code)

print(result)  # ⚠️ VULNERABLE (confidence: 94.3%)
print(result.to_dict())  # Full details as JSON

# {
#   "is_vulnerable": true,
#   "confidence": 94.3,
#   "prediction": 1,
#   "probabilities": {"safe": 0.057, "vulnerable": 0.943},
#   "errors": []
# }
```

### Batch Processing

```python
# Multiple snippets
codes = [
    "x = input(); exec(x)",
    "x = input(); sanitized = escape(x); exec(sanitized)",
    "print('hello')"
]

results = analyzer.analyze_batch(codes)

for code, result in zip(codes, results):
    status = "⚠️" if result.is_vulnerable else "✅"
    print(f"{status} {code[:30]}... ({result.confidence:.0f}%)")
```

### File/Directory Scanning

```python
# Single file
result = analyzer.analyze_file('src/app.sec')

# Entire directory
results = analyzer.analyze_directory('src/', pattern='*.sec')

for file_path, result in results.items():
    print(f"{result} {file_path}")
```

### CLI Interface

```bash
# Single code
python inference_production.py \
  --model models/secure_gnn_best.pt \
  --code "x = input(); exec(x)"

# File
python inference_production.py \
  --model models/secure_gnn_best.pt \
  --file app.sec

# Directory scan
python inference_production.py \
  --model models/secure_gnn_best.pt \
  --dir src/
```

---

## 📈 Best Practices for High Accuracy

### 1. Dataset Quality

**✅ Do:**

- Use diverse, real-world code samples
- Balance safe/vulnerable examples (50/50)
- Include multiple vulnerability types
- Use stratified train/val/test splits

**❌ Don't:**

- Use only synthetic toy examples
- Have class imbalance (>80/20)
- Reuse test data in training
- Include duplicate samples

### 2. Model Architecture

**✅ Do:**

- Use edge-aware GNN (respects DATA_DEP vs CONTROL_DEP)
- Freeze CodeBERT lower layers (transfer learning)
- Use batch normalization
- Apply dropout (0.3)

**❌ Don't:**

- Use generic GCN without edge information
- Fine-tune all CodeBERT layers (overfitting)
- Skip batch norm (training instability)
- Use excessive dropout (>0.5)

### 3. Training Strategy

**✅ Do:**

```python
# Learning rate schedule
optimizer = AdamW(model.parameters(), lr=2e-5)
scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=10, T_mult=2)

# Early stopping on F1
if val_f1 > best_f1:
    save_checkpoint()
else:
    patience_counter += 1

# Gradient clipping
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
```

**❌ Don't:**

- Use fixed learning rate
- Train until convergence (overfitting)
- Skip gradient clipping (exploding gradients)
- Use only accuracy for stopping (ignores class imbalance)

### 4. Data Augmentation (Future)

```python
# Structural: add noise to PDG edges
# Semantic: code transformations (variable renaming, comment changes)
# Temporal: train over multiple epochs with different augmentations
```

### 5. Cross-Codebase Evaluation

Test on held-out datasets:

```bash
# If you have multiple datasets
python evaluate_model.py --checkpoint models/secure_gnn_best.pt --test-data dataset/juliet_test.pt
python evaluate_model.py --checkpoint models/secure_gnn_best.pt --test-data dataset/cvegit_test.pt
```

---

## 🔧 Troubleshooting

### Issue: Out of Memory (GPU)

```bash
# Reduce batch size
# In model_config.json: "batch_size": 8  (was 16)

# OR reduce model size
# "gnn_hidden_dim": 64  (was 128)
```

### Issue: Training Diverges (NaN loss)

```bash
# Reduce learning rate
# "learning_rate": 1e-5  (was 2e-5)

# Increase gradient clipping
# "gradient_clip": 0.5  (was 1.0)

# Ensure data is normalized
```

### Issue: Validation F1 Plateaus

```bash
# Increase dataset diversity
# Add data augmentation
# Increase num_layers from 3 to 4
# Train longer (increase epochs to 100)
```

### Issue: Poor Performance on New Code

```bash
# May be overfitting to training distribution
# Collect more diverse data
# Test on different vulnerabilities
# Evaluate cross-codebase performance
```

---

## 📦 Deployment Checklist

- [ ] Model checkpoint: `models/secure_gnn_best.pt`
- [ ] Evaluation report: `logs/evaluation_report.json` (F1 > 0.80)
- [ ] Test inference: `python inference_production.py --model ... --code ...`
- [ ] API integration: Use `SecureAnalyzer` class
- [ ] Performance: Inference time <1s per sample
- [ ] Robustness: Tested on edge cases, error handling

---

## 📚 File Reference

| File                             | Purpose                                           |
| -------------------------------- | ------------------------------------------------- |
| `train_model.py`                 | Main training script with metrics & checkpointing |
| `evaluate_model.py`              | Comprehensive evaluation with confusion matrix    |
| `inference_production.py`        | Production-ready inference API                    |
| `model_config.json`              | Centralized hyperparameter configuration          |
| `models/hybrid_model.py`         | GNN + CodeBERT fusion model                       |
| `models/gnn_encoder.py`          | Edge-aware graph neural network                   |
| `models/transformer_encoder.py`  | CodeBERT semantic encoder                         |
| `models/graph_dataset.py`        | Dataset loading & batching                        |
| `dataset/build_graph_dataset.py` | Compile code → PDG → tensors                      |

---

## 🎓 Next Steps

1. **Improve Dataset**: Expand beyond synthetic data
   - Download Juliet CWE datasets
   - Add real CVE examples
   - Multi-language support

2. **Advanced Features**:
   - Attention visualization (which operations are important?)
   - Taint tracking integration
   - Explainability reports

3. **Optimization**:
   - Model quantization (faster inference)
   - Knowledge distillation (smaller model)
   - Ensemble methods

4. **Deployment**:
   - REST API (FastAPI)
   - Docker containerization
   - CI/CD integration

---

**Happy Training! 🚀**
