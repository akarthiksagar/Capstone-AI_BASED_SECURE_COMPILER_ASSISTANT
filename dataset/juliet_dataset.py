from frontend.parser.parser import parse_source
from frontend.semantic.semantic_analyzer import SemanticAnalyzer

from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer

from analysis.pdg_builder import PDGBuilder
from analysis.graph_to_pyg import GraphToPyGConverter


class SecureCompilerPipeline:

    def __init__(self):
        pass

    def compile_to_pdg(self, source_code):

        # 1️⃣ Parse
        ast = parse_source(source_code)

        # 2️⃣ Semantic analysis
        semantic = SemanticAnalyzer()
        ast.accept(semantic)

        if semantic.errors:
            return None, semantic.errors

        # 3️⃣ IR generation
        ir_builder = IRBuilder()
        cfg = ir_builder.visit_Program(ast)

        # 4️⃣ SSA transform
        ssa = SSATransformer(cfg)
        cfg = ssa.transform()

        # 5️⃣ Build PDG
        pdg_builder = PDGBuilder(cfg)
        pdg = pdg_builder.build()

        # 6️⃣ Convert to PyG
        converter = GraphToPyGConverter(pdg)
        pyg_graph = converter.convert()

        return pyg_graph, None