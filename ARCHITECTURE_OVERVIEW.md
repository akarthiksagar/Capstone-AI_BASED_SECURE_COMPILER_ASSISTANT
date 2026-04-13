# AI-Based Secure Compiler Assistant - Architecture Overview

## 1. Project Purpose and Goals

The **AI-Based Secure Compiler Assistant** is an intelligent security analysis tool that combines classical compiler techniques with machine learning to detect vulnerabilities and security flaws in code.

### Core Objectives:

- **Security-First Compilation**: Transform raw source code into intermediate representations with security awareness
- **Vulnerability Detection**: Identify common security vulnerabilities (command injection, SQL injection, tainted data flows)
- **Hybrid ML Analysis**: Combine Graph Neural Networks (GNNs) for structural analysis with Transformers for semantic understanding
- **Explainability**: Provide interpretable security insights through data/control dependence analysis
- **Language Agnostic Foundation**: Built on a custom SecureLang grammar designed for security semantics

---

## 2. Major Components and Their Responsibilities

### 2.1 Frontend (Parsing & Semantic Analysis)

**Location**: `frontend/`

The frontend transforms raw source code into an Abstract Syntax Tree (AST) with security annotations.

| Component                                               | Responsibility                                                                  |
| ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Parser Driver** (`parser_driver.py`)                  | Orchestrates ANTLR-based lexing and parsing using SecureLang grammar            |
| **AST Builder** (`ast_builder.py`)                      | Converts ANTLR parse trees into a custom AST representation                     |
| **Error Listener** (`errors/error_listener.py`)         | Captures and reports syntax errors                                              |
| **Semantic Analyzer** (`semantic/semantic_analyzer.py`) | Performs symbol table management, type checking, and security label propagation |
| **Symbol Table** (`semantic/symbol_table.py`)           | Tracks variable/function definitions across scopes                              |
| **Type System** (`semantic/type_system.py`)             | Enforces type safety and coercion rules                                         |
| **Security Labels** (`semantic/security_label.py`)      | Assigns security levels (TRUSTED, SANITIZED, UNTRUSTED, TAINTED) to variables   |
| **AST Nodes** (`ast/ast_nodes.py`)                      | Visitor pattern implementation for traversing the AST                           |

**Key Features**:

- Multi-pass analysis (function signature registration → semantic validation)
- Security label propagation through assignments and operations
- Integration with builtin function registry for knowing dangerous sinks

---

### 2.2 Middle-End (Intermediate Representation & Analysis)

**Location**: `middleend/`

The middle-end transforms the AST into lower-level representations suitable for analysis and optimization.

#### **IR Generation** (`ir/ir_builder.py`)

- Converts AST into Control Flow Graph (CFG) with IR instructions
- Generates temporary variables for complex expressions
- Flattens nested operations into basic blocks

#### **CFG Builder** (`cfg/cfg_builder.py`)

- Creates basic blocks from instruction sequences
- Manages entry/exit blocks and block successors
- Enables structured iteration over control flow

#### **Basic Blocks** (`cfg/basic_block.py`)

- Container for a sequence of IR instructions
- Tracks successor blocks for control flow edges
- Maintains predecessor relationships

#### **IR Instructions** (`ir/ir_instructions.py`)

```
- IRAssign: variable assignment
- IRBinaryOp: arithmetic/logical operations
- IRCall: function calls
- IRReturn: return statements
- IRBranch: conditional jumps
- IRJump: unconditional jumps
- IRPhi: SSA phi functions for merging values
```

#### **SSA Transformation** (`ir/ssa_transform.py`)

- Converts program into Static Single Assignment form
- Inserts phi functions at dominance frontiers
- Renames variables to track definitions uniquely
- **Pruning**: Uses liveness analysis to minimize phi nodes
- Dependencies: Dominance analysis, liveness analysis

#### **IR Security Analysis** (`security/ir_security_analysis.py`)

- Scans IR for tainted data flowing to dangerous sinks
- Detects dangerous function calls (exec, eval, system, query)
- Classifies vulnerabilities as TAINTED_SINK or TAINTED_RETURN

#### **Control Flow Analysis** (`cfg/`)

- **Dominance Analysis**: Computes immediate dominators and dominance trees
- Enables fundamental analyses (loop detection, redundancy elimination)

---

### 2.3 Analysis Layer (Advanced Program Analysis)

**Location**: `analysis/`

Sophisticated program analysis for vulnerability detection and model input generation.

#### **PDG Builder** (`pdg_builder.py`)

- Constructs Program Dependence Graph from CFG
- **Three components**:
  1. **Instruction Nodes**: Each IR instruction becomes a node with opcode and security level features
  2. **Data Dependencies**: SSA-based tracking of variable definitions and uses
  3. **Control Dependencies**: From control dependence graph (CDG)
- Identifies critical data/control paths through the program

#### **Control Dependence Graph** (`control_dependence.py`)

- Computes post-dominators and immediate post-dominators
- Determines which instructions depend on conditional branches
- Essential for detecting control-based vulnerabilities

#### **Liveness Analysis** (`liveness.py`)

- Identifies which variables are live (may be used again)
- Used for SSA phi function pruning
- Enables dead code elimination

#### **Graph Representation** (`graph_representation.py`)

- Generic graph data structure with nodes and edges
- Node features: type, opcode, security labels
- Edge types: DATA_DEP, CONTROL_DEP, CONTAINS

#### **Graph Tensorization** (`graph_tensorizer.py`)

- Converts ProgramGraph into tensors for ML models
- **Node Features**: Opcode one-hot encoding + security level embedding
- **Edge Index**: COO format for sparse adjacency
- **Edge Types**: TYPE_0 = DATA_DEP, TYPE_1 = CONTROL_DEP

#### **PyG Converter** (`graph_to_pyg.py`)

- Transforms ProgramGraph into PyTorch Geometric Data objects
- Integrates with torch_geometric for GNN processing
- Provides edge attributes for typed message passing

#### **Graph Extractor** (`graph_extractor.py`)

- Extracts CFG into graph representation
- Adds blocks, instructions, control flow, and data flow edges

#### **Explainability** (`explainability.py`)

- Extracts critical subgraphs for interpretation
- Highlights important data dependencies leading to vulnerabilities

---

## 3. Data Flow Through the System

### **Complete Analysis Pipeline**

```
SOURCE CODE (SecureLang)
    ↓
[FRONTEND]
├─ Lexer (ANTLR)
├─ Parser → Parse Tree
├─ AST Builder → AST
└─ Semantic Analyzer → AST with Security Labels + Errors
    ↓
[MIDDLE-END]
├─ IR Builder → CFG with IR Instructions
├─ SSA Transformer → SSA Form CFG
└─ IR Security Analysis → Initial Vulnerabilities
    ↓
[ANALYSIS]
├─ PDG Builder → Program Dependence Graph
│   ├─ Control Dependence Graph
│   └─ Liveness Analysis
├─ Graph Tensorizer → Tensors (X, edge_index, edge_types)
└─ PyG Converter → PyTorch Geometric Data Object
    ↓
[ML INFERENCE]
├─ GNN Encoder → Graph Embedding
├─ CodeBERT Transformer → Code Embedding
├─ Fusion Layer → Combined Representation
└─ Classification Head → [Safe, Vulnerable]
    ↓
[OUTPUT]
├─ Prediction Score & Class
├─ Semantic Errors
├─ IR Vulnerabilities
├─ PDG Visualization
└─ AST Structure
```

### **Key Data Transformations**

| Stage             | Input              | Output                   | Purpose                      |
| ----------------- | ------------------ | ------------------------ | ---------------------------- |
| Parsing           | Source Code String | AST Tree                 | Syntactic structure          |
| Semantic Analysis | AST                | AST + Security Labels    | Type safety & taint tracking |
| IR Generation     | AST                | CFG + Instructions       | Lower-level representation   |
| SSA Transform     | CFG                | SSA Form                 | Dataflow clarity             |
| PDG Building      | CFG                | Graph with nodes & edges | Dependency analysis          |
| Tensorization     | Graph              | Torch Tensors            | ML-ready format              |
| Inference         | Tensors            | Probability Logits       | Vulnerability detection      |

---

## 4. Machine Learning Models

### 4.1 Hybrid Architecture

**Location**: `models/hybrid_model.py`

The system combines two complementary encoders:

```
INPUT: (code_string, graph_data)
├─ Code String → CodeBERT Encoder
│   ├─ Tokenization (256 max tokens)
│   ├─ Transformer Layers (lower layers frozen)
│   └─ [CLS] Token Embedding (768-dim for codebert-base)
│
├─ Graph Data → GNN Encoder
│   ├─ Adjacency: edge_index + edge_types
│   ├─ Node Features: Opcode + Security Labels
│   ├─ 3-layer EdgeTypeGNNLayer stack (separate W_data, W_control)
│   └─ Graph Embedding (64-dim hidden)
│
└─ Fusion Layer
    ├─ Concatenate embeddings: (768 + 64) = 832-dim
    ├─ Linear(832 → 256) + ReLU
    ├─ Dropout(0.3)
    └─ Linear(256 → 2) → Logits [Safe, Vulnerable]
```

### 4.2 GNN Encoder

**Location**: `models/gnn_encoder.py`

- **EdgeTypeGNNLayer**: Separate linear transformations for DATA_DEP and CONTROL_DEP edges
  - Message passing: src → dst based on edge type
  - Self-loop: Maintains node self-information
- **Multiple Layers**: Captures depth-2+ dependencies
- **Output**: Node-level graph embedding via global pooling

### 4.3 CodeBERT Encoder

**Location**: `models/transformer_encoder.py`

- **Model**: microsoft/codebert-base (pre-trained on code)
- **Frozen Layers**: Lower 10 layers frozen to preserve base knowledge
- **Output**: CLS token embedding (semantic summary of code)

### 4.4 Fusion Strategy

- **Concatenation**: Combines structural (GNN) + semantic (CodeBERT) signals
- **Shared Classification Head**: Joint decision leveraging both modalities

---

## 5. Key Entry Points and API Endpoints

### 5.1 Command-Line Interfaces

**`main.py`** - Development/testing entry point

- Contains commented examples for dataset testing
- Loads graphs and performs test inference

**`inference.py`** - Model inference script

```python
analyze_code(code, model):
    - Compiles code to PDG
    - Runs model inference
    - Outputs "✅ Safe" or "⚠️ Vulnerable"
```

### 5.2 REST API Server

**`api_server.py`** - Flask-based web service

```
POST /api/analyze
{
    "code": "<source code>"
}

Response:
{
    "success": true,
    "prediction": "safe|vulnerable",
    "security_score": 0-100,
    "semantic_errors": [
        {
            "id": "sem_0",
            "message": "...",
            "line": 5,
            "column": 3,
            "severity": "ERROR|WARNING",
            "security_related": true,
            "type": "error|warning",
            "category": "Security|Semantic"
        }
    ],
    "ir_vulnerabilities": [
        {
            "type": "TAINTED_SINK",
            "function": "exec",
            "severity": "HIGH"
        }
    ],
    "pdg": {
        "nodes": [...],
        "edges": [...]
    },
    "ir_blocks": [
        {"name": "block_0", "instructions": ["IRAssign", "IRCall"]}
    ],
    "ast_text": "Program\n├─FunctionDef\n..."
}
```

**Features**:

- Multi-stage analysis pipeline
- Semantic error reporting
- IR-level vulnerability detection
- PDG structure visualization
- CORS enabled for frontend integration

### 5.3 Web Dashboard

**`ui_for_capstone/`** - Next.js React frontend

**Components**:

- **Dashboard Header**: Navigation and project info
- **Code Editor**: Syntax-highlighted SecureLang editor
- **Security Panel**: Lists detected issues with line references
- **Dependency Graph**: Visual PDG rendering
- **AI Assistant**: Interactive guidance
- **Stats Cards**: Summary metrics (Shield icon, AlertTriangle, Bug, CheckCircle)

**Sample Built-in Codes**:

- `sql_injection.sec`: Demonstrates taint flow to SQL sink
- `safe_code.sec`: Clean arithmetic operations
- `syntax_error.sec`: Intentional syntax error for error handling

---

## 6. Compiler Frontend, Middle-End, and Backend Structure

### 6.1 **Frontend** (Parsing & Semantics)

```
SecureLang Grammar (grammar/SecureLang.g4)
    ↓
ANTLR Lexer & Parser (generated/)
    ↓
Parse Tree
    ↓
AST Builder Pattern
    ↓
Abstract Syntax Tree (AST Nodes)
    ↓
Semantic Analysis Visitor
    ├─ Symbol Table Management
    ├─ Type Checking
    ├─ Security Label Propagation  ← KEY: Taint Tracking
    └─ Error Collection
```

**Grammar Features** (SecureLang.g4):

- Function definitions with parameter lists
- Control flow: if/else, while, for loops
- Assignment and expression statements
- Import statements
- Comments

### 6.2 **Middle-End** (IR & Optimization)

```
AST
    ↓
IR Builder (Visitor Pattern)
    ├─ Basic Block Creation
    ├─ Instruction Flattening
    └─ Temporary Variable Generation
    ↓
Control Flow Graph (CFG)
    ↓
Dominance Analysis
    ↓
SSA Transformation
    ├─ Phi Function Insertion (at dominance frontiers)
    ├─ Liveness-based Pruning
    └─ Variable Renaming
    ↓
SSA-Form CFG + IR Security Analysis
```

**IR Instruction Set**:

- Data flow: Assignment, Binary operations
- Control flow: Branch, Jump
- Call semantics: Function calls
- SSA: Phi functions for join points
- Security annotations on each instruction

### 6.3 **Backend** (Analysis & ML)

```
SSA-Form CFG
    ↓
PDG Construction
    ├─ Add Instruction Nodes
    ├─ Data Dependencies (SSA-based)
    ├─ Control Dependencies (CDG)
    └─ Program Dependence Graph
    ↓
Graph Feature Extraction
    ├─ Node Features: Opcode, Security Level, Features
    ├─ Edge Types: Data, Control
    └─ Sparse Adjacency Matrix
    ↓
Tensorization
    ├─ One-hot Opcodes
    ├─ Security Level Embeddings
    ├─ Edge Index (COO format)
    └─ PyTorch Tensors
    ↓
ML Inference
    ├─ GNN → Graph Embedding
    ├─ CodeBERT → Text Embedding
    ├─ Fusion → Combined Embedding
    └─ Classification → Confidence Scores
```

---

## 7. Dataset and Training Pipeline

### 7.1 Dataset Sources

**Juliet Dataset**:

- Location: `dataset/juliet_*.json`
- CWE-based synthetic C test cases
- High volume of labeled security examples
- Processed variants:
  - `juliet_processed.json` - Full dataset
  - `juliet_processed_dedup.json` - Deduplicated
  - `juliet_balanced.json` - Class-balanced
  - `juliet_securelang.json` - Converted to SecureLang

**Synthetic Dataset**:

- Location: `dataset/secure_synthetic_10k.json`
- Generated safe/vulnerable code samples
- Patterns simulated: input sanitization, sinks, authentication checks
- Script: `dataset/juliet_dataset.py` - Random vulnerability generator
  - Command injection patterns
  - Data flow obfuscation with noise blocks
  - Sanitized vs. unsanitized variants

### 7.2 Dataset Processing Pipeline

```
Raw Juliet CWE Dataset
    ↓
Juliet Converter (`dataset/juliet_converter/`)
├─ juliet_loader.py: Load CWE test cases
├─ c_ast_extractor.py: Extract AST from C code
├─ c_to_securelang.py: Translate C → SecureLang
├─ juliet_text_extractor.py: Extract source text
└─ fake_headers/: Standard C library stubs
    ↓
SecureLang Dataset
    ↓
Graph Dataset Building (`dataset/build_graph_dataset.py`)
├─ Parse → AST
├─ Semantic Analysis
├─ IR Generation
├─ SSA Transform
├─ PDG Building
├─ Tensorization
    ├─ Node Features (X)
    ├─ Edge Index
    ├─ Edge Types
    └─ Labels
    ↓
PyTorch Graph Dataset (`dataset/graph_dataset.pt`)
    Contains: [X, edge_index, edge_types, label, code]
```

### 7.3 Training Pipelines

**Graph-Based Training** (`models/train_hybrid.py`):

```python
1. Load graph_dataset.pt
2. DataLoader with batch_size=16
3. Hybrid Model forward pass:
   - GNN on graph tensors
   - CodeBERT on code strings
   - Fusion classification
4. Cross-entropy loss optimization
5. Validation on held-out 20%
```

**Standalone Training** (`models/train.py`):

```python
1. Load secure_synthetic_10k.json
2. Dataset with:
   - Tokenized code (CodeBERT)
   - Simple graph features (count-based: if, while, sinks, etc.)
3. HybridModel with CodeBERT + FC layers
4. Cross-entropy loss + SGD optimizer
```

**Key Hyperparameters**:

- Batch size: 16
- Epochs: 5
- Max token length: 256
- LR: Typically 1e-4 to 1e-5
- Dropout: 0.3

### 7.4 Pre-trained Models

**Stored Models**:

- `models/hybrid_model.pt` - Trained hybrid architecture
- `models/graph_dataset.pt` - Tensorized graph training set

**Dependency**:

- CodeBERT (`microsoft/codebert-base`): 768-dim embeddings, pre-trained on code

---

## 8. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  WEB DASHBOARD (Next.js)                │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │ Code Editor  │ │Security Panel│ │Dependency Graph│ │
│  └──────┬───────┘ └──────▲───────┘ └────────▲────────┘ │
│         │                │                  │           │
└─────────┼────────────────┼──────────────────┼───────────┘
          │                │                  │
          POST /api/analyze (JSON)            │
          │                │                  │
┌─────────▼────────────────┼──────────────────┼───────────┐
│       REST API SERVER (Flask)                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │        /api/analyze Route Handler              │    │
│  └──────────────────┬──────────────────────────────┘    │
└─────────────────────┼──────────────────────────────────┘
                      │
┌─────────────────────▼──────────────────────────────────┐
│          ANALYSIS PIPELINE (Python)                     │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 1. FRONTEND: parse_source()                    │    │
│  │    └─ Lexer → Parser → AST + Semantic Labels  │    │
│  │                                                │    │
│  │ 2. MIDDLE-END: IR + SSA                       │    │
│  │    └─ CFG → SSA Form → IR Analysis            │    │
│  │                                                │    │
│  │ 3. ANALYSIS: PDG Construction                 │    │
│  │    └─ Control/Data Dependencies → Graph       │    │
│  │                                                │    │
│  │ 4. TENSORIZATION: To ML Format                │    │
│  │    └─ Tensors (X, edge_index, types) + Code  │    │
│  │                                                │    │
│  │ 5. ML INFERENCE: Hybrid Model                 │    │
│  │    ├─ GNN(graph tensors) → Embedding         │    │
│  │    ├─ CodeBERT(code) → Embedding             │    │
│  │    ├─ Fusion → Classification                 │    │
│  │    └─ [Safe, Vulnerable] Confidence          │    │
│  │                                                │    │
│  │ 6. OUTPUT: JSON Response                      │    │
│  │    ├─ Prediction + Score                     │    │
│  │    ├─ Semantic Errors                        │    │
│  │    ├─ IR Vulnerabilities                     │    │
│  │    ├─ PDG Structure                          │    │
│  │    └─ AST Visualization                      │    │
│  │                                                │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Database Layer:                                        │
│  ├─ dataset/graph_dataset.pt (training data)          │
│  ├─ models/hybrid_model.pt (pre-trained weights)     │
│  └─ grammar/SecureLang.g4 (language definition)      │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Security Model: Taint Tracking

### **Security Labels** (`frontend/semantic/security_label.py`)

```python
enum SecurityLevel:
    TRUSTED = 0       # Known safe sources (constants, literals)
    SANITIZED = 1     # After filtering/escaping
    UNTRUSTED = 2     # User input, external data
    TAINTED = 3       # Dangerous level detected
```

### **Taint Propagation Rules**

1. **Sources**: Variables assigned from `input()` → UNTRUSTED
2. **Joins**: Combine labels with max operation (UNTRUSTED > SANITIZED > TRUSTED)
3. **Sanitizers**: Functions like `sanitize()`, `validate()`, `escape()` lower level to SANITIZED
4. **Sinks**: Dangerous functions (exec, eval, db_query, etc.) trigger vulnerability alerts
5. **Returns**: Tainted returns flagged as medium-severity vulnerabilities

### **Example Vulnerability Path**

```securelang
user_input = input()              // UNTRUSTED
query = "SELECT * FROM users WHERE id = " + user_input  // UNTRUSTED propagates
exec(query)                       // TAINTED_SINK vulnerability!
```

---

## 10. Critical Data Structures

### **AST Node Hierarchy**

- `ASTNode` (base)
  - `Program` → list of statements
  - `FunctionDef` → name, params, body
  - `IfStatement`, `WhileStatement`, `ForStatement`
  - `Assignment`, `FunctionCall`
  - `BinaryOp`, `UnaryOp`
  - `Identifier`, `Literal`

### **IR Instruction Hierarchy**

- `IRInstruction` (base with security_label)
  - `IRAssign`, `IRBinaryOp`, `IRCall`
  - `IRReturn`, `IRBranch`, `IRJump`
  - `IRPhi` (SSA join points)

### **Graph Representation**

- `ProgramGraph`
  - `GraphNode`: id, type, features
  - `GraphEdge`: source, target, type (DATA_DEP, CONTROL_DEP)

### **Tensor Formats**

- `X`: Node feature matrix (num_nodes × feature_dim)
- `edge_index`: COO format adjacency (2 × num_edges)
- `edge_types`: Edge type labels (num_edges)

---

## 11. Workflow Summary

### **Development Workflow**

1. Write/edit SecureLang code in web editor
2. Submit for analysis via `/api/analyze`
3. Backend processes through full pipeline
4. ML model predicts vulnerability + confidence
5. Results displayed with interactive PDG visualization

### **Training Workflow**

1. Load Juliet dataset or synthetic generator
2. Convert to SecureLang
3. Build graph dataset (compile → PDG → tensorize)
4. Train hybrid model (GNN + CodeBERT + fusion)
5. Save pre-trained weights for inference

### **Integration Points**

- **Parser ↔ Semantic**: AST visitor pattern
- **IR ↔ CFG**: Builder pattern during traversal
- **SSA ↔ Dominance**: External dependency computation
- **PDG ↔ Tensorizer**: Graph representation abstraction
- **Tensors ↔ ML Model**: PyTorch data structure
- **API ↔ ML**: JSON serialization of model outputs

---

## 12. Key Technical Insights

### **Why This Architecture?**

1. **Multi-Stage Frontend**: Separates syntax (parsing) from semantics (type/security checking) for modularity and error reporting
2. **SSA Conversion**: Enables precise data flow analysis; phi functions mark value merging points
3. **Dual-Modality ML**: GNNs capture structural vulnerability patterns (control/data flows), Transformers capture semantic intent (context, operations)
4. **Graph Tensorization**: Encodes both topology and node/edge semantics efficiently for hardware acceleration
5. **Taint Tracking**: Explicit security label propagation enables high-precision vulnerability detection
6. **Explainability**: PDG extraction and critical subgraph highlighting support interpretable results

### **Limitations & Future Work**

- **Language Scope**: Limited to SecureLang; requires translation from real languages (C, Python, Java)
- **Model Training**: Graph dataset construction is computationally expensive
- **Accuracy**: Hybrid model trained on synthetic data; may not generalize to real-world code patterns
- **Scalability**: PDG construction is O(n²) worst-case for complex programs
- **Real-time Analysis**: API latency depends on code size and model inference speed

---

## 13. File Organization Quick Reference

```
Capstone-AI_BASED_SECURE_COMPILER_ASSISTANT/
├─ frontend/              # Parsing & semantic analysis
│  ├─ parser_driver.py   # ANTLR orchestration
│  ├─ ast_builder.py     # Parse tree → AST
│  ├─ semantic/          # Type checking & taint tracking
│  │  ├─ semantic_analyzer.py
│  │  ├─ symbol_table.py
│  │  ├─ security_label.py
│  │  └─ ...
│  ├─ ast/              # AST node definitions
│  ├─ errors/           # Error handling
│  └─ grammar/          # ANTLR grammar & generated lexer/parser
│
├─ middleend/            # IR & optimization
│  ├─ ir/               # Intermediate representation
│  │  ├─ ir_builder.py
│  │  ├─ ir_instructions.py
│  │  ├─ ssa_transform.py
│  │  └─ ...
│  ├─ cfg/              # Control flow graph
│  │  ├─ cfg_builder.py
│  │  ├─ basic_block.py
│  │  └─ dominance.py
│  └─ security/         # IR-level security analysis
│     └─ ir_security_analysis.py
│
├─ analysis/             # Advanced program analysis
│  ├─ pdg_builder.py    # Program dependence graph
│  ├─ control_dependence.py
│  ├─ liveness.py
│  ├─ graph_representation.py
│  ├─ graph_extractor.py
│  ├─ graph_tensorizer.py
│  ├─ graph_to_pyg.py
│  └─ explainability.py
│
├─ models/              # ML models & training
│  ├─ hybrid_model.py   # Fusion architecture
│  ├─ gnn_encoder.py
│  ├─ transformer_encoder.py
│  ├─ train_hybrid.py
│  └─ ...
│
├─ dataset/             # Data preparation
│  ├─ graph_dataset.py
│  ├─ build_graph_dataset.py
│  ├─ juliet_*.json     # Training data
│  └─ juliet_converter/ # C to SecureLang
│
├─ pipeline/            # End-to-end compilation
│  └─ compiler_pipeline.py
│
├─ api_server.py        # Flask REST API
├─ inference.py         # Model inference script
│
└─ ui_for_capstone/     # Next.js web dashboard
   └─ app/, components/, lib/, ...
```

---

This architecture represents a sophisticated blend of classical compiler design and modern machine learning, enabling security-aware code analysis through multiple complementary lenses.
