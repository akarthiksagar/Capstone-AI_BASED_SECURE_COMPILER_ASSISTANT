from pipeline.compiler_pipeline import SecureCompilerPipeline
from frontend.parser_driver import parse_source
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from analysis.graph_tensorizer import GraphTensorizer

code = """
x = input()
if x {
    y = x + 1
}
else {
    y = 0
}
return y

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
