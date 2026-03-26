# Code Vulnerability Detection via Graph Neural Networks

A research + engineering project that detects security vulnerabilities in source code using Graph Neural Networks (GNN) across multiple program graph representations: **AST**, **CFG**, **PDG**, and **CPG**.

---

## Motivation

Static analysis tools often rely on hand-crafted rules and miss subtle vulnerabilities. This project explores whether learning-based methods — particularly GNNs operating on program graphs — can outperform classical ML baselines (SVM, MLP, GBDT) and sequence-based models (Transformer) on binary vulnerability classification.

---

## Project Structure

```
vulnerability-detection/
│
├── README.md
├── requirements.txt
│
├── embedding/                   # Step 1: convert code → vectors
│   ├── embed_graph.py           # Doc2Vec embedding for graph-based models
│   └── embed_non_graph.py       # Embedding for non-graph models (SVM, MLP, etc.)
│
├── models/
│   ├── gnn/                     # GNN per graph type
│   │   ├── gnn_ast.py           # GNN on Abstract Syntax Tree
│   │   ├── gnn_cfg.py           # GNN on Control Flow Graph
│   │   ├── gnn_cpg.py           # GNN on Code Property Graph
│   │   └── gnn_pdg.py           # GNN on Program Dependence Graph
│   │
│   ├── classical/               # Non-graph baselines
│   │   ├── svm.py
│   │   ├── mlp.py
│   │   └── gbdt.py
│   │
│   ├── transformer/
│   │   └── transformer.py       # Transformer-based sequence model
│   │
│   └── combined/                # Multi-graph experiments
│       ├── all_models.py        # Run all models and compare
│       └── combine.py           # Graph fusion / ensemble
│
├── data/                        # Dataset files (not tracked by git)
│   └── .gitkeep
│
└── utils/
    └── metrics.py               # Shared evaluation: Accuracy, F1, Precision, Recall
```

---

## Pipeline Overview

```
Raw source code (labeled JSONL)
        │
        ▼
  [embedding/]  ←── Doc2Vec (100-dim vectors)
        │
        ▼
  [models/gnn/]  ←── DGL GraphConv (2-layer GNN)
        │
        ▼
  Binary classification: vulnerable (1) / clean (0)
        │
        ▼
  [utils/metrics.py]  ←── Accuracy, F1, Precision, Recall
```

---

## Graph Representations

| Graph Type | Abbr. | What it captures |
|---|---|---|
| Abstract Syntax Tree | AST | Syntactic structure of code |
| Control Flow Graph | CFG | Execution paths and branching logic |
| Program Dependence Graph | PDG | Data and control dependencies |
| Code Property Graph | CPG | Unified AST + CFG + PDG |

---

## Models Compared

| Model | Type | Input |
|---|---|---|
| GNN (GraphConv) | Graph-based | AST / CFG / PDG / CPG embeddings |
| GraphSAGE | Graph-based | All graph types |
| Transformer | Sequence-based | Token-level code embeddings |
| SVM | Classical ML | Flat code vectors |
| MLP | Classical ML | Flat code vectors |
| GBDT | Classical ML | Flat code vectors |

---

## Quickstart

### 1. Install dependencies

```bash
pip install torch dgl gensim scikit-learn matplotlib
```

### 2. Prepare embeddings

```bash
python embedding/embed_graph.py
```

### 3. Train and evaluate a GNN

```bash
python models/gnn/gnn_cpg.py
```

### 4. Run all models and compare

```bash
python models/combined/all_models.py
```

---

## Dataset

This project uses the [Devign dataset](https://sites.google.com/view/devign) — a large-scale C/C++ vulnerability dataset extracted from open-source projects (QEMU, FFmpeg, etc.), with binary labels indicating whether each function contains a vulnerability.

> Place your labeled JSONL files under `data/` before running embedding scripts.

---

## Results (Example)

| Model | Graph | Accuracy | F1 | Precision | Recall |
|---|---|---|---|---|---|
| GNN | CPG | — | — | — | — |
| GNN | PDG | — | — | — | — |
| GNN | CFG | — | — | — | — |
| GNN | AST | — | — | — | — |
| GraphSAGE | CPG | — | — | — | — |
| Transformer | — | — | — | — | — |
| SVM | — | — | — | — | — |
| MLP | — | — | — | — | — |
| GBDT | — | — | — | — | — |

> Fill in your actual results after running experiments.

---

## Key Design Choices

- **Doc2Vec** is used to embed code tokens into fixed-size vectors, enabling GNNs to process heterogeneous graph nodes uniformly.
- **DGL** (Deep Graph Library) powers the GNN layers with efficient sparse graph operations.
- **GraphConv** with 2 layers and ReLU activation serves as the base GNN architecture; GraphSAGE is compared as an inductive alternative.
- **CPG** combines structural and semantic information from AST, CFG, and PDG — expected to provide the richest signal for vulnerability detection.

---

## License

MIT
