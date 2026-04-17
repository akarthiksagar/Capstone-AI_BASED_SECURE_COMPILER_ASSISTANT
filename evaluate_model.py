"""
Comprehensive Model Evaluation Pipeline
========================================

Evaluate trained model on test set with:
- Per-class metrics (precision, recall, F1)
- Confusion matrix
- Vulnerability type breakdown
- Explainability analysis
- Cross-codebase generalization tests
"""

import os
import json
import argparse
from pathlib import Path
import numpy as np
from tqdm import tqdm
import logging
from collections import defaultdict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

from models.hybrid_model import HybridModel
from models.graph_dataset import SecureGraphDataset, graph_collate_fn

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# =====================================================
# MODEL LOADING
# =====================================================

def load_checkpoint(checkpoint_path, device):
    """Load model from checkpoint."""
    logger.info(f"Loading checkpoint from {checkpoint_path}...")
    
    checkpoint = torch.load(checkpoint_path, map_location=device)
    config = checkpoint['config']
    
    # Recreate model
    model = HybridModel(
        graph_input_dim=config['model']['graph_input_dim'],
        num_gnn_layers=config['gnn']['num_layers'],
        gnn_hidden_dim=config['model']['gnn_hidden_dim'],
        dropout=config['gnn']['dropout']
    )
    
    model.load_state_dict(checkpoint['model_state'])
    model = model.to(device)
    model.eval()
    
    logger.info(f"✓ Model loaded (trained for {checkpoint['epoch']+1} epochs)")
    
    return model, config


# =====================================================
# EVALUATION METRICS
# =====================================================

class EvaluationMetrics:
    """Compute and track evaluation metrics."""
    
    def __init__(self, num_classes=2):
        self.num_classes = num_classes
        self.all_preds = []
        self.all_labels = []
        self.all_probs = []
        self.vulnerabilities = defaultdict(lambda: {'preds': [], 'labels': []})
    
    def add_batch(self, preds, labels, probs=None, vuln_types=None):
        """Add batch predictions and labels."""
        self.all_preds.extend(preds)
        self.all_labels.extend(labels)
        
        if probs is not None:
            self.all_probs.extend(probs)
        
        if vuln_types is not None:
            for pred, label, vuln in zip(preds, labels, vuln_types):
                self.vulnerabilities[vuln]['preds'].append(pred)
                self.vulnerabilities[vuln]['labels'].append(label)
    
    def compute_metrics(self):
        """Compute all metrics."""
        metrics = {}
        
        # Overall metrics
        metrics['accuracy'] = accuracy_score(self.all_labels, self.all_preds)
        metrics['precision_0'] = precision_score(self.all_labels, self.all_preds, pos_label=0, zero_division=0)
        metrics['precision_1'] = precision_score(self.all_labels, self.all_preds, pos_label=1, zero_division=0)
        metrics['recall_0'] = recall_score(self.all_labels, self.all_preds, pos_label=0, zero_division=0)
        metrics['recall_1'] = recall_score(self.all_labels, self.all_preds, pos_label=1, zero_division=0)
        metrics['f1_0'] = f1_score(self.all_labels, self.all_preds, pos_label=0, zero_division=0)
        metrics['f1_1'] = f1_score(self.all_labels, self.all_preds, pos_label=1, zero_division=0)
        
        if len(self.all_probs) > 0:
            metrics['auc_roc'] = roc_auc_score(self.all_labels, self.all_probs)
        
        # Per-vulnerability metrics
        vuln_metrics = {}
        for vuln_type, data in self.vulnerabilities.items():
            if len(data['labels']) > 0:
                preds = data['preds']
                labels = data['labels']
                vuln_metrics[vuln_type] = {
                    'accuracy': accuracy_score(labels, preds),
                    'precision': precision_score(labels, preds, zero_division=0),
                    'recall': recall_score(labels, preds, zero_division=0),
                    'f1': f1_score(labels, preds, zero_division=0),
                    'samples': len(labels)
                }
        
        metrics['per_vulnerability'] = vuln_metrics
        
        return metrics
    
    def confusion_matrix_analysis(self):
        """Compute confusion matrix."""
        cm = confusion_matrix(self.all_labels, self.all_preds)
        
        # Visualize
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['Safe', 'Vulnerable'],
                    yticklabels=['Safe', 'Vulnerable'])
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Confusion Matrix')
        plt.savefig('logs/confusion_matrix.png', dpi=100, bbox_inches='tight')
        plt.close()
        
        return cm


# =====================================================
# EVALUATION LOOP
# =====================================================

@torch.no_grad()
def evaluate_model(model, test_loader, device):
    """Evaluate model on test set."""
    model.eval()
    
    metrics = EvaluationMetrics()
    
    logger.info("Evaluating model...")
    for batch in tqdm(test_loader, desc="Evaluation"):
        X = batch['X'].to(device)
        edge_index = batch['edge_index'].to(device)
        edge_types = batch['edge_types'].to(device)
        batch_ids = batch['batch_ids'].to(device)
        code_list = batch['code_list']
        labels = batch['label'].to(device)
        
        # Forward pass
        logits = model(X, edge_index, edge_types, batch_ids, code_list, device)
        probs = torch.softmax(logits, dim=1)[:, 1].cpu().numpy()
        preds = torch.argmax(logits, dim=1).cpu().numpy()
        
        metrics.add_batch(preds, labels.cpu().numpy(), probs)
    
    return metrics


# =====================================================
# ERROR ANALYSIS
# =====================================================

def analyze_errors(metrics, test_data, device):
    """Analyze misclassified samples."""
    logger.info("\n" + "="*60)
    logger.info("ERROR ANALYSIS")
    logger.info("="*60)
    
    false_positives = []
    false_negatives = []
    
    for i, (pred, label) in enumerate(zip(metrics.all_preds, metrics.all_labels)):
        if pred != label:
            if pred == 1 and label == 0:
                false_positives.append(i)
            else:
                false_negatives.append(i)
    
    logger.info(f"False Positives: {len(false_positives)} (Safe code flagged as vulnerable)")
    logger.info(f"False Negatives: {len(false_negatives)} (Vulnerable code missed)")
    
    if false_positives:
        logger.info("\nExample False Positive:")
        idx = false_positives[0]
        logger.info(f"  Code: {test_data[idx]['code'][:100]}...")
    
    if false_negatives:
        logger.info("\nExample False Negative:")
        idx = false_negatives[0]
        logger.info(f"  Code: {test_data[idx]['code'][:100]}...")


# =====================================================
# REPORT GENERATION
# =====================================================

def generate_report(metrics, model_path, save_dir='logs'):
    """Generate comprehensive evaluation report."""
    os.makedirs(save_dir, exist_ok=True)
    
    report_data = {
        'model_path': model_path,
        'metrics': metrics.compute_metrics(),
        'confusion_matrix': metrics.confusion_matrix_analysis().tolist()
    }
    
    # Save JSON report
    report_path = f'{save_dir}/evaluation_report.json'
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    logger.info(f"\n✓ Report saved to {report_path}")
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("EVALUATION SUMMARY")
    logger.info("="*60)
    
    metrics_computed = report_data['metrics']
    logger.info(f"\nOverall Performance:")
    logger.info(f"  Accuracy:  {metrics_computed['accuracy']:.4f}")
    logger.info(f"  Precision (Safe/Vulnerable):    {metrics_computed['precision_0']:.4f} / {metrics_computed['precision_1']:.4f}")
    logger.info(f"  Recall    (Safe/Vulnerable):    {metrics_computed['recall_0']:.4f} / {metrics_computed['recall_1']:.4f}")
    logger.info(f"  F1-Score  (Safe/Vulnerable):    {metrics_computed['f1_0']:.4f} / {metrics_computed['f1_1']:.4f}")
    
    if 'auc_roc' in metrics_computed:
        logger.info(f"  AUC-ROC:   {metrics_computed['auc_roc']:.4f}")
    
    if metrics_computed['per_vulnerability']:
        logger.info(f"\nPer-Vulnerability Type Performance:")
        for vuln_type, vuln_metrics in metrics_computed['per_vulnerability'].items():
            logger.info(f"  {vuln_type} ({vuln_metrics['samples']} samples):")
            logger.info(f"    F1: {vuln_metrics['f1']:.4f}, Recall: {vuln_metrics['recall']:.4f}")
    
    logger.info("="*60 + "\n")


# =====================================================
# MAIN
# =====================================================

def main():
    parser = argparse.ArgumentParser(description='Evaluate Secure Compiler GNN')
    parser.add_argument('--checkpoint', type=str, required=True, help='Checkpoint path')
    parser.add_argument('--test-data', type=str, default='dataset/test_graphs.pt', help='Test data path')
    parser.add_argument('--device', type=str, default='auto', help='Device')
    args = parser.parse_args()
    
    # Device
    if args.device == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(args.device)
    
    logger.info(f"Device: {device}\n")
    
    # Load model
    model, config = load_checkpoint(args.checkpoint, device)
    
    # Load test data
    logger.info(f"Loading test data from {args.test_data}...")
    if not Path(args.test_data).exists():
        raise FileNotFoundError(f"Test data not found: {args.test_data}")
    
    test_data = torch.load(args.test_data)
    test_dataset = SecureGraphDataset(test_data)
    test_loader = DataLoader(
        test_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=False,
        collate_fn=graph_collate_fn
    )
    
    logger.info(f"Test samples: {len(test_data)}\n")
    
    # Evaluate
    metrics = evaluate_model(model, test_loader, device)
    
    # Analysis
    analyze_errors(metrics, test_data, device)
    
    # Report
    generate_report(metrics, args.checkpoint)


if __name__ == '__main__':
    main()
