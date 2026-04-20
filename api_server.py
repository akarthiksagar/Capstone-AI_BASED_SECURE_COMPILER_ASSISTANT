import os
import re
import traceback
import math
from pathlib import Path
from flask import Flask, request, jsonify

try:
    from flask_cors import CORS
except ImportError:
    CORS = None

# Compiler Pipeline
from frontend.parser_driver import parse_source
from frontend.parser_driver import ParseSyntaxError
from frontend.ast.ast_base import ASTNode
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from middleend.security.ir_security_analysis import IRSecurityAnalyzer
from translation.universal_translator import UniversalTranslator, TranslationSyntaxError

try:
    from inference_production import SecureAnalyzer
except ImportError as ex:
    SecureAnalyzer = None
    print(f"Warning: model analyzer unavailable: {ex}")

app = Flask(__name__)
if CORS is not None:
    CORS(app)  # Enable CORS for all domains for development
else:
    print("Warning: flask_cors not installed, CORS support disabled.")

translator = UniversalTranslator()

def resolve_model_path() -> str:
    explicit = os.environ.get("SECURE_ANALYZER_MODEL_PATH")
    if explicit:
        return explicit

    candidates = [
        "models/secure_gnn_best.pt",
        "models/hybrid_model.pt",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return candidates[0]

def is_compatible_model_checkpoint(model_path: str) -> bool:
    path = Path(model_path)
    if not path.exists():
        return False

    try:
        import torch
        checkpoint = torch.load(path, map_location="cpu")
    except Exception:
        return False

    if not isinstance(checkpoint, dict):
        return False

    if "model_state" in checkpoint and "config" in checkpoint:
        return True

    # Plain state_dict checkpoints from older layouts are not compatible with
    # the current SecureAnalyzer reconstruction path.
    return False

MODEL_PATH = resolve_model_path()
model_analyzer = None
if SecureAnalyzer is not None:
    if is_compatible_model_checkpoint(MODEL_PATH):
        try:
            model_analyzer = SecureAnalyzer(model_path=MODEL_PATH)
        except Exception as ex:
            print(f"Warning: SecureAnalyzer failed to initialize. Model inference disabled. {ex}")
    else:
        print(f"Info: No compatible model checkpoint available at {MODEL_PATH}. Model inference disabled.")
else:
    print("Warning: SecureAnalyzer is not available because its dependencies are missing.")

def detect_language(code: str) -> str:
    code = code.strip()
    if re.search(r'^\s*#include\b', code, re.M):
        return 'c'
    if re.search(r'\bprintf\(|\bscanf\(|\bstrcpy\(|\bgets\(', code):
        return 'c'
    if re.search(r'\bfunction\b|console\.log\(|document\.|window\.', code):
        return 'javascript'
    if re.search(r'\bvar\b|\blet\b|\bconst\b', code) and re.search(r'\bfunction\b', code):
        return 'javascript'
    if re.search(r'^\s*def\s+\w+\(', code, re.M):
        return 'python'
    if re.search(r'\bimport\s+\w+|\bfrom\s+\w+\s+import\b', code):
        return 'python'
    return 'securelang'

@app.route('/api/analyze', methods=['POST'])
def analyze():
    print("DEBUG: Received /api/analyze request")
    data = request.json
    if not data or 'code' not in data:
        return jsonify({"success": False, "error": "No code provided"}), 400

    code = data['code']
    language = data.get('language')
    if language and language.lower() in ['auto', 'detect', 'default']:
        language = None
    language = language or detect_language(code)
    translated_code = code

    try:
        if language not in ['securelang', 'secure_lang']:
            translated_code = translator.translate(code, language)
    except TranslationSyntaxError as ex:
        return jsonify({
            "success": False,
            "error": ex.message,
            "language": ex.language,
            "error_type": "syntax"
        }), 400

    response = {
        "success": True,
        "prediction": "safe",
        "security_score": 100,
        "semantic_errors": [],
        "ir_vulnerabilities": [],
        "pdg": {
            "nodes": [],
            "edges": []
        },
        "ir_blocks": [],
        "ast_text": "",
        "detected_language": language,
        "translated_code": translated_code,
        "model_enabled": model_analyzer is not None,
        "model_path": MODEL_PATH,
        "model_result": None
    }

    try:
        # 1. Parsing
        print("DEBUG: Starting parsing")
        ast = parse_source(translated_code)
        
        def is_ast_like(value):
            return isinstance(value, ASTNode)

        def ast_tree_to_str(node, indent=0):
            if not is_ast_like(node):
                return ""

            res = "  " * indent + node.__class__.__name__ + "\n"
            for attr in vars(node).values():
                if isinstance(attr, list):
                    for item in attr:
                        if is_ast_like(item):
                            res += ast_tree_to_str(item, indent + 1)
                elif is_ast_like(attr):
                    res += ast_tree_to_str(attr, indent + 1)
            return res

        try:
            response["ast_text"] = ast_tree_to_str(ast)
        except Exception as ast_ex:
            print(f"Warning: failed to build ast_text: {ast_ex}")
            response["ast_text"] = "AST visualization unavailable"
        print("DEBUG: Parsing done")

        # 2. Semantic Analysis
        print("DEBUG: Starting semantic analysis")
        semantic = SemanticAnalyzer()
        ast.accept(semantic)

        for i, err in enumerate(semantic.errors):
            severity_str = err.severity.name if hasattr(err.severity, 'name') else str(err.severity)
            
            response["semantic_errors"].append({
                "id": f"sem_{i}",
                "message": err.message,
                "line": err.line,
                "column": err.column,
                "severity": severity_str,
                "security_related": getattr(err, "security_related", False),
                "type": "error" if severity_str == "ERROR" else "warning",
                "category": "Security" if getattr(err, "security_related", False) else "Semantic"
            })

        if semantic.errors:
            # If semantic analysis errors out entirely, return early with findings
            pass 

        # 3. IR Generation
        print("DEBUG: Starting IR generation")
        ir_builder = IRBuilder()
        cfg = ast.accept(ir_builder)

        # 4. SSA Transformation
        ssa = SSATransformer(cfg)
        cfg = ssa.transform()

        # Build structural IR blocks response
        for block in cfg.blocks:
            instructions = [instr.__class__.__name__ for instr in block.instructions]
            response["ir_blocks"].append({
                "name": block.name,
                "instructions": instructions
            })

        # 5. Execute IR Security Analysis
        print("DEBUG: Starting IR security analysis")
        security_analyzer = IRSecurityAnalyzer(cfg)
        ir_vulns = security_analyzer.analyze()

        for i, vuln in enumerate(ir_vulns):
            vtype = vuln.get("type")
            title = f"Tainted Sink: {vuln.get('function')}" if vtype == "TAINTED_SINK" else "Tainted Return"
            desc = f"Untrusted data flows into dangerous function {vuln.get('function')}." if vtype == "TAINTED_SINK" else "Untrusted data is returned from the function."

            response["ir_vulnerabilities"].append({
                "id": f"ir_{i}",
                "type": vtype,
                "function": vuln.get("function"),
                "severity": "high",
                "line": None,
                "title": title,
                "description": desc,
                "category": "Taint Flow"
            })

        # 6. PDG Construction for Node Map
        print("DEBUG: Starting PDG construction")
        pdg_builder = PDGBuilder(cfg)
        pdg = pdg_builder.build()

        # Layout simple circle
        nodes_len = max(1, len(pdg.nodes))
        radius = 40
        for i, (n_id, node) in enumerate(pdg.nodes.items()):
            sec_level = str(node.features.get("security_level", ""))
            
            if "TAINTED" in sec_level or "UNTRUSTED" in sec_level:
                node_type = "vulnerable"
            elif "TRUSTED" in sec_level:
                node_type = "safe"
            else:
                node_type = "warning"

            response["pdg"]["nodes"].append({
                "id": str(n_id),
                "label": node.features.get("opcode", "Unknown"),
                "x": 50 + radius * math.cos(i * 2 * math.pi / nodes_len),
                "y": 50 + radius * math.sin(i * 2 * math.pi / nodes_len),
                "type": node_type
            })

        for edge in pdg.edges:
            response["pdg"]["edges"].append({
                "from": str(edge.source),
                "to": str(edge.target)
            })

        # 7. Compute Final Status
        print("DEBUG: Computing final status")
        num_critical = sum(1 for e in response["semantic_errors"] if e["severity"] == "ERROR")
        num_high = len(response["ir_vulnerabilities"])
        
        score = 100 - (num_critical * 20) - (num_high * 15) - (len(response["semantic_errors"]) * 5)
        response["security_score"] = max(0, score)

        if model_analyzer is not None:
            model_result = model_analyzer.analyze(translated_code)
            response["model_result"] = model_result.to_dict()
            if model_result.is_vulnerable:
                response["prediction"] = "vulnerable"
            response["security_score"] = max(response["security_score"], int(model_result.confidence))

        if response["security_score"] < 100 or num_critical > 0 or num_high > 0:
            response["prediction"] = "vulnerable"

        print("DEBUG: Analysis complete")
        return jsonify(response)

    except Exception as e:
        if isinstance(e, ParseSyntaxError):
            return jsonify({
                "success": False,
                "error": str(e),
                "language": language,
                "error_type": "syntax"
            }), 400
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
