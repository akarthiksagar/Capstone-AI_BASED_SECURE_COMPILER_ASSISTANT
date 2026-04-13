import os
import traceback
import math
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS

# Compiler Pipeline
from frontend.parser_driver import parse_source
from frontend.semantic.semantic_analyzer import SemanticAnalyzer
from middleend.ir.ir_builder import IRBuilder
from middleend.ir.ssa_transform import SSATransformer
from analysis.pdg_builder import PDGBuilder
from middleend.security.ir_security_analysis import IRSecurityAnalyzer

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains for development

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data or 'code' not in data:
        return jsonify({"success": False, "error": "No code provided"}), 400

    code = data['code']

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
        "ast_text": ""
    }

    try:
        # 1. Parsing
        ast = parse_source(code)
        
        def ast_tree_to_str(node, indent=0):
            res = "  " * indent + node.__class__.__name__ + "\n"
            for attr in vars(node).values():
                if isinstance(attr, list):
                    for item in attr:
                        if hasattr(item, "__class__"):
                            res += ast_tree_to_str(item, indent + 1)
                elif hasattr(attr, "__class__") and hasattr(attr, "accept"):
                    res += ast_tree_to_str(attr, indent + 1)
            return res

        response["ast_text"] = ast_tree_to_str(ast)

        # 2. Semantic Analysis
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
        num_critical = sum(1 for e in response["semantic_errors"] if e["severity"] == "ERROR")
        num_high = len(response["ir_vulnerabilities"])
        
        score = 100 - (num_critical * 20) - (num_high * 15) - (len(response["semantic_errors"]) * 5)
        response["security_score"] = max(0, score)

        if response["security_score"] < 100 or num_critical > 0 or num_high > 0:
            response["prediction"] = "vulnerable"

        return jsonify(response)

    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
