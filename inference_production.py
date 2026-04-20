"""
Production-Ready Inference Interface
====================================

Clean, unified interface for vulnerability detection.

Usage:
  from inference_production import SecureAnalyzer
  
  analyzer = SecureAnalyzer(model_path='models/secure_gnn_best.pt')
  result = analyzer.analyze(code)
  print(result)
"""

import os
import json
from pathlib import Path
import logging
from collections import OrderedDict

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    nn = None
    TORCH_AVAILABLE = False

from typing import Dict, List, Tuple, Optional

from pipeline.compiler_pipeline import SecureCompilerPipeline
from models.hybrid_model import HybridModel

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =====================================================
# RESULT DATACLASSES
# =====================================================

class VulnerabilityResult:
    """Structured result from vulnerability analysis."""
    
    def __init__(
        self,
        is_vulnerable: bool,
        confidence: float,
        prediction: int,
        probabilities: Dict[str, float],
        errors: List[str] = None,
        vulnerabilities: List[Dict] = None,
        graph_stats: Dict = None
    ):
        self.is_vulnerable = is_vulnerable
        self.confidence = confidence  # 0-100
        self.prediction = prediction  # 0 (safe) or 1 (vulnerable)
        self.probabilities = probabilities
        self.errors = errors or []
        self.vulnerabilities = vulnerabilities or []
        self.graph_stats = graph_stats or {}
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            'is_vulnerable': self.is_vulnerable,
            'confidence': self.confidence,
            'prediction': self.prediction,
            'probabilities': self.probabilities,
            'errors': self.errors,
            'vulnerabilities': self.vulnerabilities,
            'graph_stats': self.graph_stats
        }
    
    def __repr__(self) -> str:
        status = "⚠️ VULNERABLE" if self.is_vulnerable else "✅ SAFE"
        return f"{status} (confidence: {self.confidence:.1f}%)"


# =====================================================
# SECURE ANALYZER
# =====================================================

class SecureAnalyzer:
    """Main vulnerability detection interface."""
    
    def __init__(
        self,
        model_path: str,
        device: str = 'auto',
        confidence_threshold: float = 0.5
    ):
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch is required for SecureAnalyzer but is not installed.")
        """
        Initialize the analyzer.
        
        Args:
            model_path: Path to trained model checkpoint
            device: 'cuda', 'cpu', or 'auto'
            confidence_threshold: Threshold for vulnerability classification
        """
        self.device = self._init_device(device)
        self.model = self._load_model(model_path)
        self.pipeline = SecureCompilerPipeline()
        self.confidence_threshold = confidence_threshold
        
        logger.info(f"✓ SecureAnalyzer initialized (device: {self.device})")
    
    def _init_device(self, device: str) -> torch.device:
        """Initialize device."""
        if device == 'auto':
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        return torch.device(device)
    
    def _load_model(self, model_path: str) -> HybridModel:
        """Load trained model from checkpoint."""
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        checkpoint = torch.load(model_path, map_location=self.device)
        config = checkpoint.get('config') if isinstance(checkpoint, dict) else None
        state_dict = checkpoint

        if isinstance(checkpoint, dict) and 'model_state' in checkpoint:
            state_dict = checkpoint['model_state']
        if config is None:
            config = self._load_model_config()
        
        # Recreate model
        model = HybridModel(
            graph_input_dim=config['model']['graph_input_dim'],
            num_gnn_layers=config['gnn']['num_layers'],
            gnn_hidden_dim=config['model']['gnn_hidden_dim'],
            dropout=config['gnn']['dropout']
        )
        
        model.load_state_dict(state_dict)
        model = model.to(self.device)
        model.eval()
        
        logger.info(f"✓ Model loaded from {model_path}")
        return model

    def _load_model_config(self) -> dict:
        """Load model settings when a checkpoint does not bundle config."""
        config_path = Path('model_config.json')
        if not config_path.exists():
            raise FileNotFoundError("model_config.json not found for model reconstruction")
        with config_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    
    @torch.no_grad()
    def analyze(self, code: str) -> VulnerabilityResult:
        """
        Analyze code for vulnerabilities.
        
        Args:
            code: Source code to analyze
        
        Returns:
            VulnerabilityResult with predictions and confidence
        """
        try:
            # Compile to PDG
            pyg_graph, errors = self.pipeline.compile_to_pdg(code)
            
            if pyg_graph is None:
                # Compilation failed
                return VulnerabilityResult(
                    is_vulnerable=False,
                    confidence=0.0,
                    prediction=0,
                    probabilities={'safe': 0.5, 'vulnerable': 0.5},
                    errors=errors if errors else ["Compilation failed"]
                )
            
            # Extract features
            X = pyg_graph.x.to(self.device)
            edge_index = pyg_graph.edge_index.to(self.device)
            edge_types = pyg_graph.edge_attr.long().to(self.device) if pyg_graph.edge_attr is not None else torch.zeros(edge_index.shape[1], dtype=torch.long, device=self.device)
            
            # Create batch info (single graph)
            batch_ids = torch.zeros(X.shape[0], dtype=torch.long, device=self.device)
            
            # Forward pass
            logits = self.model(X, edge_index, edge_types, batch_ids, [code], self.device)
            probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
            pred = int(torch.argmax(logits[0]))
            
            # Compute confidence
            confidence = float(probs[pred]) * 100
            
            # Determine if vulnerable based on prediction
            is_vulnerable = (pred == 1)
            
            # Graph statistics
            graph_stats = {
                'num_nodes': int(X.shape[0]),
                'num_edges': int(edge_index.shape[1]),
                'avg_node_features': int(X.shape[1])
            }
            
            return VulnerabilityResult(
                is_vulnerable=is_vulnerable,
                confidence=confidence,
                prediction=pred,
                probabilities={
                    'safe': float(probs[0]),
                    'vulnerable': float(probs[1])
                },
                graph_stats=graph_stats
            )
        
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}", exc_info=True)
            return VulnerabilityResult(
                is_vulnerable=False,
                confidence=0.0,
                prediction=0,
                probabilities={'safe': 0.5, 'vulnerable': 0.5},
                errors=[str(e)]
            )
    
    def analyze_batch(self, code_list: List[str]) -> List[VulnerabilityResult]:
        """
        Analyze multiple code snippets.
        
        Args:
            code_list: List of code strings
        
        Returns:
            List of VulnerabilityResult objects
        """
        results = []
        for code in code_list:
            results.append(self.analyze(code))
        return results
    
    def analyze_file(self, file_path: str) -> VulnerabilityResult:
        """
        Analyze code from file.
        
        Args:
            file_path: Path to code file
        
        Returns:
            VulnerabilityResult
        """
        with open(file_path, 'r') as f:
            code = f.read()
        return self.analyze(code)
    
    def analyze_directory(self, dir_path: str, pattern: str = '*.sec') -> Dict[str, VulnerabilityResult]:
        """
        Analyze all code files in directory.
        
        Args:
            dir_path: Directory path
            pattern: File pattern to match
        
        Returns:
            Dictionary mapping file paths to results
        """
        results = {}
        dir_path = Path(dir_path)
        
        for file_path in dir_path.glob(f'**/{pattern}'):
            try:
                result = self.analyze_file(str(file_path))
                results[str(file_path)] = result
            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {e}")
        
        return results


# =====================================================
# CLI INTERFACE
# =====================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Secure Compiler - Vulnerability Detection')
    parser.add_argument('--model', type=str, required=True, help='Model checkpoint path')
    parser.add_argument('--code', type=str, help='Code string to analyze')
    parser.add_argument('--file', type=str, help='Code file to analyze')
    parser.add_argument('--dir', type=str, help='Directory to scan')
    parser.add_argument('--device', type=str, default='auto', help='Device (auto/cuda/cpu)')
    parser.add_argument('--threshold', type=float, default=0.5, help='Confidence threshold')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = SecureAnalyzer(
        model_path=args.model,
        device=args.device,
        confidence_threshold=args.threshold
    )
    
    # Analyze based on input
    if args.code:
        result = analyzer.analyze(args.code)
        print("\nAnalysis Result:")
        print(json.dumps(result.to_dict(), indent=2))
    
    elif args.file:
        result = analyzer.analyze_file(args.file)
        print(f"\n{args.file}:")
        print(json.dumps(result.to_dict(), indent=2))
    
    elif args.dir:
        results = analyzer.analyze_directory(args.dir)
        print(f"\nScanned {len(results)} files:")
        for file_path, result in results.items():
            status = "⚠️ VULNERABLE" if result.is_vulnerable else "✅ SAFE"
            print(f"  {status} {file_path} ({result.confidence:.1f}%)")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
