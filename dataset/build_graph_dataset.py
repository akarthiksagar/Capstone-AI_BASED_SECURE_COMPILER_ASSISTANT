import json
import torch
from tqdm import tqdm

from frontend.parser_driver import parse_source
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from analysis.graph_tensorizer import GraphTensorizer


INPUT_FILE = "dataset/secure_synthetic_10k.json"
OUTPUT_FILE = "dataset/graph_dataset.pt"


def compile_to_graph(code):

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

    return X, edge_index, edge_types


def main():

    with open(INPUT_FILE, "r") as f:
        dataset = json.load(f)

    graph_data = []

    for sample in tqdm(dataset):

        code = sample["code"]
        label = sample["label"]

        try:
            X, edge_index, edge_types = compile_to_graph(code)

            graph_data.append({
                "X": X,
                "edge_index": edge_index,
                "edge_types": edge_types,
                "label": torch.tensor(label, dtype=torch.long),
                "code":code
            })

        except Exception as e:
            print("Compilation failed, skipping sample:", e)

    torch.save(graph_data, OUTPUT_FILE)
    print("Saved graph dataset to", OUTPUT_FILE)


if __name__ == "__main__":
    main()