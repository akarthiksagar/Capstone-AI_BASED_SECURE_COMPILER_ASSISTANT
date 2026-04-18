import json
import torch
from tqdm import tqdm
import argparse
import sys
from pathlib import Path

# Ensure project root is importable when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from translation.universal_translator import UniversalTranslator
from frontend.parser_driver import parse_source
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from analysis.graph_tensorizer import GraphTensorizer

def compile_to_graph(code, translator=None, original_lang=None):
    """Compile code to graph, translating if needed"""
    if translator and original_lang and original_lang != 'securelang':
        code = translator.translate(code, original_lang)

    try:
        # Parse
        ast = parse_source(code)

        # Semantic
        semantic = SemanticAnalyzer()
        ast.accept(semantic)

        # IR
        ir_builder = IRBuilder()
        cfg = ir_builder.visit_Program(ast)

        # SSA
        ssa = SSATransformer(cfg)
        cfg = ssa.transform()

        # PDG
        pdg_builder = PDGBuilder(cfg)
        pdg = pdg_builder.build()

        # Tensorize
        tensorizer = GraphTensorizer()
        X, edge_index, edge_types = tensorizer.tensorize(pdg)

        return X, edge_index, edge_types, None  # Success
    except Exception as e:
        return None, None, None, str(e)  # Error

def build_multi_source_dataset(input_file, output_file, max_samples=None):
    """Build dataset from multi-source collected data"""
    with open(input_file, 'r') as f:
        dataset = json.load(f)

    translator = UniversalTranslator()
    graph_data = []
    successful = 0
    failed = 0

    for i, sample in enumerate(tqdm(dataset[:max_samples] if max_samples else dataset)):
        code = sample.get('code', '')
        if not code.strip():
            continue

        lang = sample.get('language', 'unknown')
        vulnerable = sample.get('vulnerable', False)

        X, edge_index, edge_types, error = compile_to_graph(code, translator, lang)

        if X is not None:
            graph_data.append({
                'id': i,
                'code': code,
                'language': lang,
                'label': 1 if vulnerable else 0,  # 1 = vulnerable, 0 = safe
                'X': X,
                'edge_index': edge_index,
                'edge_types': edge_types,
                'source': sample.get('source', 'unknown'),
                'metadata': {k: v for k, v in sample.items() if k not in ['code', 'X', 'edge_index', 'edge_types']}
            })
            successful += 1
        else:
            failed += 1
            if failed < 10:  # Log first few errors
                print(f"Failed to compile sample {i}: {error}")

    print(f"Successfully compiled {successful} samples, failed {failed}")

    # Split into train/val/test
    train_size = int(0.7 * len(graph_data))
    val_size = int(0.15 * len(graph_data))

    splits = {
        'train': graph_data[:train_size],
        'val': graph_data[train_size:train_size + val_size],
        'test': graph_data[train_size + val_size:]
    }

    for split_name, split_data in splits.items():
        torch.save(split_data, f"dataset/{split_name}_graphs.pt")

    # Save full dataset
    torch.save(graph_data, output_file)
    print(f"Saved dataset to {output_file}")

    # Save statistics
    stats = {
        'total_samples': len(graph_data),
        'vulnerable': sum(1 for s in graph_data if s['label'] == 1),
        'safe': sum(1 for s in graph_data if s['label'] == 0),
        'sources': {},
        'languages': {}
    }

    for sample in graph_data:
        src = sample.get('source', 'unknown')
        lang = sample.get('language', 'unknown')
        stats['sources'][src] = stats['sources'].get(src, 0) + 1
        stats['languages'][lang] = stats['languages'].get(lang, 0) + 1

    with open('dataset/dataset_stats.json', 'w') as f:
        json.dump(stats, f, indent=2)

    print("Dataset statistics:")
    print(json.dumps(stats, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Build Multi-Source Graph Dataset")
    parser.add_argument("--input", default="dataset/multi_source_dataset.json", help="Input dataset file")
    parser.add_argument("--output", default="dataset/multi_source_graph_dataset.pt", help="Output graph dataset")
    parser.add_argument("--max-samples", type=int, help="Maximum samples to process")
    args = parser.parse_args()

    build_multi_source_dataset(args.input, args.output, args.max_samples)

if __name__ == "__main__":
    main()
