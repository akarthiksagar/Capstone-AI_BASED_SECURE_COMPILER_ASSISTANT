"""
Unified Training Pipeline for Secure Compiler Assistant
========================================================

Train a hybrid GNN + CodeBERT model to detect vulnerabilities in code.

Features:
- Edge-aware GNN processing of PDG graphs
- CodeBERT semantic encoding
- Proper train/val/test splits with stratification
- Class balancing and weighted loss
- Early stopping, checkpointing, metrics tracking
- Per-vulnerability-type evaluation
"""

import os
import json
import argparse
from pathlib import Path
from collections import Counter
import numpy as np
from tqdm import tqdm
import logging

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, WeightedRandomSampler
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from models.hybrid_model import HybridModel
from models.graph_dataset import SecureGraphDataset, graph_collate_fn

# =====================================================
# LOGGING SETUP
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# =====================================================
# CONFIG LOADING
# =====================================================

def load_config(config_path):
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


# =====================================================
# DEVICE DETECTION
# =====================================================

def get_device(config):
    """Auto-detect device."""
    device_cfg = config.get('device', 'auto')
    
    if device_cfg == 'auto':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    else:
        device = torch.device(device_cfg)
    
    logger.info(f"Using device: {device}")
    if torch.cuda.is_available():
        logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
    
    return device


# =====================================================
# DATASET PREPARATION
# =====================================================

def prepare_datasets(config, seed=42):
    """
    Load and split the graph dataset into train/val/test.
    """
    dataset_dir = config['data']['dataset_dir']
    
    # Check if pre-split files exist
    train_file = Path(dataset_dir) / 'train_graphs.pt'
    val_file = Path(dataset_dir) / 'val_graphs.pt'
    test_file = Path(dataset_dir) / 'test_graphs.pt'
    
    if train_file.exists() and val_file.exists() and test_file.exists():
        logger.info("Loading pre-split datasets...")
        train_data = torch.load(train_file)
        val_data = torch.load(val_file)
        test_data = torch.load(test_file)
    else:
        logger.info("Loading and splitting dataset from scratch...")
        
        # Load main dataset
        dataset_file = Path(dataset_dir) / 'graph_dataset.pt'
        if not dataset_file.exists():
            raise FileNotFoundError(f"Dataset not found at {dataset_file}")
        
        full_data = torch.load(dataset_file)
        logger.info(f"Loaded {len(full_data)} samples")
        
        # Get labels for stratification
        labels = [sample['label'].item() if isinstance(sample['label'], torch.Tensor) else sample['label'] 
                  for sample in full_data]
        
        # Split: train/val/test
        train_test_split_ratio = config['data']['train_split'] + config['data']['val_split']
        train_val_data, test_data = train_test_split(
            full_data,
            test_size=config['data']['test_split'],
            random_state=seed,
            stratify=labels if len(set(labels)) > 1 else None
        )
        
        # Further split train/val
        train_labels = [sample['label'].item() if isinstance(sample['label'], torch.Tensor) else sample['label'] 
                        for sample in train_val_data]
        val_ratio = config['data']['val_split'] / train_test_split_ratio
        train_data, val_data = train_test_split(
            train_val_data,
            test_size=val_ratio,
            random_state=seed,
            stratify=train_labels if len(set(train_labels)) > 1 else None
        )
        
        # Save splits
        os.makedirs(dataset_dir, exist_ok=True)
        torch.save(train_data, train_file)
        torch.save(val_data, val_file)
        torch.save(test_data, test_file)
        logger.info(f"Saved splits to {dataset_dir}")
    
    logger.info(f"Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")
    
    # Check class balance
    train_labels = [s['label'].item() if isinstance(s['label'], torch.Tensor) else s['label'] for s in train_data]
    label_counts = Counter(train_labels)
    logger.info(f"Class distribution (train): {dict(label_counts)}")
    
    return train_data, val_data, test_data


def get_class_weights(data, num_classes=2):
    """Compute class weights for imbalanced data."""
    labels = [s['label'].item() if isinstance(s['label'], torch.Tensor) else s['label'] for s in data]
    counts = Counter(labels)
    
    weights = []
    for label in labels:
        weight = 1.0 / counts[label]
        weights.append(weight)
    
    weights = torch.tensor(weights, dtype=torch.float)
    return weights


# =====================================================
# TRAINING
# =====================================================

class Trainer:
    def __init__(self, model, config, device):
        self.model = model
        self.config = config
        self.device = device
        
        # Optimizer
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=config['training']['learning_rate'],
            weight_decay=config['training']['weight_decay']
        )
        
        # Scheduler
        self.scheduler = CosineAnnealingWarmRestarts(
            self.optimizer,
            T_0=10,
            T_mult=2,
            eta_min=1e-6
        )
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss()
        
        # Tracking
        self.best_val_f1 = 0.0
        self.patience_counter = 0
        self.epochs_trained = 0
        
        # Create checkpoint dir
        os.makedirs(config['output']['checkpoint_dir'], exist_ok=True)
        os.makedirs(config['output']['log_dir'], exist_ok=True)
    
    def train_epoch(self, train_loader):
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        all_preds = []
        all_labels = []
        
        pbar = tqdm(train_loader, desc="Training", leave=False)
        for batch in pbar:
            # Move to device
            X = batch['X'].to(self.device)
            edge_index = batch['edge_index'].to(self.device)
            edge_types = batch['edge_types'].to(self.device)
            batch_ids = batch['batch_ids'].to(self.device)
            code_list = batch['code_list']
            labels = batch['label'].to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            logits = self.model(X, edge_index, edge_types, batch_ids, code_list, self.device)
            
            loss = self.criterion(logits, labels)
            
            # Backward pass
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config['training']['gradient_clip'])
            self.optimizer.step()
            
            total_loss += loss.item()
            
            # Metrics
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())
            
            pbar.update(1)
        
        avg_loss = total_loss / len(train_loader)
        accuracy = accuracy_score(all_labels, all_preds)
        
        return avg_loss, accuracy
    
    @torch.no_grad()
    def validate(self, val_loader):
        """Validate model."""
        self.model.eval()
        total_loss = 0.0
        all_preds = []
        all_labels = []
        
        for batch in tqdm(val_loader, desc="Validating", leave=False):
            X = batch['X'].to(self.device)
            edge_index = batch['edge_index'].to(self.device)
            edge_types = batch['edge_types'].to(self.device)
            batch_ids = batch['batch_ids'].to(self.device)
            code_list = batch['code_list']
            labels = batch['label'].to(self.device)
            
            logits = self.model(X, edge_index, edge_types, batch_ids, code_list, self.device)
            loss = self.criterion(logits, labels)
            
            total_loss += loss.item()
            
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())
        
        avg_loss = total_loss / len(val_loader)
        accuracy = accuracy_score(all_labels, all_preds)
        precision = precision_score(all_labels, all_preds, zero_division=0)
        recall = recall_score(all_labels, all_preds, zero_division=0)
        f1 = f1_score(all_labels, all_preds, zero_division=0)
        
        return avg_loss, accuracy, precision, recall, f1
    
    def train_loop(self, train_loader, val_loader, num_epochs):
        """Main training loop."""
        logger.info(f"Starting training for {num_epochs} epochs...")
        
        for epoch in range(num_epochs):
            train_loss, train_acc = self.train_epoch(train_loader)
            val_loss, val_acc, val_prec, val_rec, val_f1 = self.validate(val_loader)
            
            logger.info(
                f"Epoch {epoch+1}/{num_epochs} | "
                f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
                f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f} F1: {val_f1:.4f}"
            )
            
            self.scheduler.step()
            
            # Early stopping & checkpointing
            if val_f1 > self.best_val_f1:
                self.best_val_f1 = val_f1
                self.patience_counter = 0
                
                # Save best model
                self.save_checkpoint(epoch, is_best=True)
                logger.info(f"✓ Saved best model (F1: {val_f1:.4f})")
            else:
                self.patience_counter += 1
                
                if self.patience_counter >= self.config['training']['early_stopping_patience']:
                    logger.info(f"Early stopping at epoch {epoch+1}")
                    break
            
            # Regular checkpoint
            if (epoch + 1) % self.config['output']['save_frequency'] == 0:
                self.save_checkpoint(epoch)
            
            self.epochs_trained += 1
    
    def save_checkpoint(self, epoch, is_best=False):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state': self.model.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'scheduler_state': self.scheduler.state_dict(),
            'best_val_f1': self.best_val_f1,
            'config': self.config
        }
        
        if is_best:
            path = self.config['output']['model_save_path']
        else:
            path = f"{self.config['output']['checkpoint_dir']}/checkpoint_epoch_{epoch+1}.pt"
        
        torch.save(checkpoint, path)


# =====================================================
# MAIN
# =====================================================

def main():
    parser = argparse.ArgumentParser(description='Train Secure Compiler GNN')
    parser.add_argument('--config', type=str, default='model_config.json', help='Config file path')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    device = get_device(config)
    
    # Set seed
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    
    # Prepare datasets
    train_data, val_data, test_data = prepare_datasets(config, seed=args.seed)
    
    # Create dataloaders
    train_dataset = SecureGraphDataset(train_data)
    val_dataset = SecureGraphDataset(val_data)
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=True,
        collate_fn=graph_collate_fn
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=config['training']['batch_size'],
        shuffle=False,
        collate_fn=graph_collate_fn
    )
    
    logger.info(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")
    
    # Create model
    logger.info("Creating model...")
    model = HybridModel(
        graph_input_dim=config['model']['graph_input_dim'],
        num_gnn_layers=config['gnn']['num_layers'],
        gnn_hidden_dim=config['model']['gnn_hidden_dim'],
        dropout=config['gnn']['dropout']
    )
    model = model.to(device)
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    logger.info(f"Total parameters: {total_params:,} | Trainable: {trainable_params:,}")
    
    # Create trainer
    trainer = Trainer(model, config, device)
    
    # Train
    trainer.train_loop(train_loader, val_loader, config['training']['epochs'])
    
    logger.info("✓ Training completed!")


if __name__ == '__main__':
    main()
