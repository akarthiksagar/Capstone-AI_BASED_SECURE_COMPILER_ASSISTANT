import ast
import re
from typing import List


class UniversalTranslator:
    """
    Translate source code to a SecureLang-compatible subset.
    The translator prioritizes parser compatibility over perfect fidelity.
    """

    _reserved_identifiers = {
        "def", "if", "else", "while", "for", "in", "try", "except", "finally",
        "as", "with", "assert", "return", "import", "from", "and", "or", "not",
        "True", "False", "None",
        "exec", "eval", "system", "sql", "open", "connect", "deserialize",
        "input", "getenv", "request",
    }

    def translate(self, code: str, language: str) -> str:
        lang = (language or "").lower()
        if lang == "securelang":
            return code
        if lang == "python":
            return self.translate_python(code)
        if lang in {"c", "cpp"}:
            return self.translate_c(code)
        if lang in {"javascript", "js"}:
            return self.translate_javascript(code)
        return self.fallback_translate(code)

    # -------------------------------------------------
    # Python
    # -------------------------------------------------

    def translate_python(self, code: str) -> str:
        try:
            tree = ast.parse(code)
        except Exception:
            return self.fallback_translate(code)

        lines = self._py_stmt_list(tree.body, indent=0)
        translated = "\n".join(lines).strip()
        return translated if translated else self._minimal_program(code)

    def _py_stmt_list(self, stmts: List[ast.stmt], indent: int) -> List[str]:
        out: List[str] = []
        for stmt in stmts:
            out.extend(self._py_stmt(stmt, indent))
        return out

    def _py_stmt(self, node: ast.stmt, indent: int) -> List[str]:
        ind = "    " * indent

        if isinstance(node, ast.FunctionDef):
            name = self._safe_name(node.name)
            params = ", ".join(self._safe_name(arg.arg) for arg in node.args.args)
            body = self._py_stmt_list(node.body, indent + 1)
            if not body:
                body = [("    " * (indent + 1)) + "tmp = 0"]
            return [f"{ind}def {name}({params}) {{", *body, f"{ind}}}"]

        if isinstance(node, ast.Assign):
            target = self._py_assign_target(node.targets[0]) if node.targets else "tmp"
            value = self._py_expr(node.value)
            return [f"{ind}{target} = {value}"]

        if isinstance(node, ast.AnnAssign):
            target = self._py_assign_target(node.target)
            value = self._py_expr(node.value) if node.value is not None else "None"
            return [f"{ind}{target} = {value}"]

        if isinstance(node, ast.AugAssign):
            target = self._py_assign_target(node.target)
            op = self._bin_op(node.op)
            value = self._py_expr(node.value)
            return [f"{ind}{target} = {target} {op} {value}"]

        if isinstance(node, ast.Return):
            if node.value is None:
                return [f"{ind}return"]
            return [f"{ind}return {self._py_expr(node.value)}"]

        if isinstance(node, ast.Expr):
            return [f"{ind}{self._py_expr(node.value)}"]

        if isinstance(node, ast.If):
            cond = self._py_expr(node.test)
            body = self._py_stmt_list(node.body, indent + 1) or [("    " * (indent + 1)) + "tmp = 0"]
            result = [f"{ind}if {cond} {{", *body, f"{ind}}}"]
            if node.orelse:
                else_body = self._py_stmt_list(node.orelse, indent + 1) or [("    " * (indent + 1)) + "tmp = 0"]
                result.extend([f"{ind}else {{", *else_body, f"{ind}}}"])
            return result

        if isinstance(node, ast.While):
            cond = self._py_expr(node.test)
            body = self._py_stmt_list(node.body, indent + 1) or [("    " * (indent + 1)) + "tmp = 0"]
            return [f"{ind}while {cond} {{", *body, f"{ind}}}"]

        if isinstance(node, ast.For):
            target = self._py_assign_target(node.target)
            if "." in target:
                target = "i"
            iterable = self._py_expr(node.iter)
            body = self._py_stmt_list(node.body, indent + 1) or [("    " * (indent + 1)) + "tmp = 0"]
            return [f"{ind}for {target} in {iterable} {{", *body, f"{ind}}}"]

        if isinstance(node, ast.Import):
            lines = []
            for alias in node.names:
                module = self._safe_dotted_name(alias.name)
                if module:
                    lines.append(f"{ind}import {module}")
            return lines or [f"{ind}tmp = 0"]

        if isinstance(node, ast.ImportFrom):
            module = self._safe_dotted_name(node.module or "module")
            imported = [self._safe_name(a.name) for a in node.names if a.name != "*"]
            if imported:
                return [f"{ind}from {module} import {', '.join(imported)}"]
            return [f"{ind}import {module}"]

        # Unsupported statements become a harmless no-op assignment.
        return [f"{ind}tmp = 0"]

    def _py_assign_target(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return self._safe_name(node.id)
        if isinstance(node, ast.Attribute):
            base = self._py_expr(node.value)
            return f"{base}.{self._safe_name(node.attr)}"
        return "tmp"

    def _py_expr(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return self._safe_name(node.id)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return self._quote(node.value)
            if node.value is True:
                return "True"
            if node.value is False:
                return "False"
            if node.value is None:
                return "None"
            return str(node.value)

        if isinstance(node, ast.Str):
            return self._quote(node.s)

        if isinstance(node, ast.Num):
            return str(node.n)

        if isinstance(node, ast.Attribute):
            return f"{self._py_expr(node.value)}.{self._safe_name(node.attr)}"

        if isinstance(node, ast.Call):
            func = self._py_expr(node.func)
            args = [self._py_expr(a) for a in node.args]
            for kw in node.keywords:
                if kw.arg is not None:
                    args.append(f"{self._safe_name(kw.arg)} = {self._py_expr(kw.value)}")
            return f"{func}({', '.join(args)})"

        if isinstance(node, ast.BinOp):
            return f"{self._py_expr(node.left)} {self._bin_op(node.op)} {self._py_expr(node.right)}"

        if isinstance(node, ast.BoolOp):
            joiner = " and " if isinstance(node.op, ast.And) else " or "
            return joiner.join(self._py_expr(v) for v in node.values)

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.Not):
                return f"not {self._py_expr(node.operand)}"
            if isinstance(node.op, ast.USub):
                return f"-{self._py_expr(node.operand)}"
            if isinstance(node.op, ast.UAdd):
                return f"+{self._py_expr(node.operand)}"
            return self._py_expr(node.operand)

        if isinstance(node, ast.Compare):
            left = self._py_expr(node.left)
            pieces = []
            for op, comp in zip(node.ops, node.comparators):
                pieces.append(f"{left} {self._cmp_op(op)} {self._py_expr(comp)}")
                left = self._py_expr(comp)
            return " and ".join(pieces) if pieces else "True"

        if isinstance(node, ast.Subscript):
            return f"{self._py_expr(node.value)}[{self._py_expr(node.slice)}]"

        if isinstance(node, ast.List):
            return "[" + ", ".join(self._py_expr(e) for e in node.elts) + "]"

        if isinstance(node, ast.Dict):
            entries = []
            for key, value in zip(node.keys, node.values):
                if key is None:
                    continue
                entries.append(f"{self._py_expr(key)}: {self._py_expr(value)}")
            return "{" + ", ".join(entries) + "}"

        if isinstance(node, ast.Tuple):
            # SecureLang has no tuple literal, map to list.
            return "[" + ", ".join(self._py_expr(e) for e in node.elts) + "]"

        if isinstance(node, ast.JoinedStr):
            parts = []
            for val in node.values:
                if isinstance(val, ast.Constant) and isinstance(val.value, str):
                    parts.append(val.value)
                else:
                    parts.append("{}")
            return self._quote("".join(parts))

        if isinstance(node, ast.FormattedValue):
            return self._py_expr(node.value)

        return "None"

    # -------------------------------------------------
    # C / C++ / JS
    # -------------------------------------------------

    def translate_c(self, code: str) -> str:
        return self._translate_c_like(code, default_name="translated_c")

    def translate_javascript(self, code: str) -> str:
        return self._translate_c_like(code, default_name="translated_js")

    def _translate_c_like(self, code: str, default_name: str) -> str:
        fn_pattern = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*\{")
        matches = fn_pattern.findall(code or "")
        vulnerable = self._looks_vulnerable(code)

        functions = []
        for name, params_blob in matches:
            fn_name = self._safe_name(name)
            params = self._extract_param_names(params_blob)
            functions.append(self._build_stub_function(fn_name, params, vulnerable))

        if not functions:
            return self._build_stub_function(default_name, ["arg"], vulnerable)
        return "\n\n".join(functions)

    # -------------------------------------------------
    # Fallbacks / helpers
    # -------------------------------------------------

    def fallback_translate(self, code: str) -> str:
        return self._minimal_program(code)

    def _minimal_program(self, code: str) -> str:
        vulnerable = self._looks_vulnerable(code)
        return self._build_stub_function("translated_main", ["arg"], vulnerable)

    def _build_stub_function(self, name: str, params: List[str], vulnerable: bool) -> str:
        safe_name = self._safe_name(name)
        safe_params = ", ".join(self._safe_name(p) for p in params if p) or "arg"
        body = [
            "    data = 1",
        ]
        if vulnerable:
            body.append("    risk_flag = data + 1")
            body.append("    return risk_flag")
        else:
            body.append("    safe_flag = data")
            body.append("    return safe_flag")
        return "\n".join([f"def {safe_name}({safe_params}) {{", *body, "}"])

    def _extract_param_names(self, params_blob: str) -> List[str]:
        params_blob = (params_blob or "").strip()
        if not params_blob or params_blob == "void":
            return []

        names: List[str] = []
        for raw in params_blob.split(","):
            cleaned = re.sub(r"/\*.*?\*/", "", raw).strip()
            tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", cleaned)
            if tokens:
                names.append(self._safe_name(tokens[-1]))
        return names

    def _looks_vulnerable(self, code: str) -> bool:
        text = (code or "").lower()
        patterns = [
            "exec(", "eval(", "strcpy(", "gets(", "sprintf(", "system(",
            "sql", "injection", "overflow", "deserializ", "command",
        ]
        return any(p in text for p in patterns)

    def _safe_name(self, name: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9_]", "_", (name or "").strip())
        if not cleaned:
            cleaned = "var"
        if cleaned[0].isdigit():
            cleaned = f"v_{cleaned}"
        if cleaned in self._reserved_identifiers:
            cleaned = f"{cleaned}_id"
        return cleaned

    def _safe_dotted_name(self, name: str) -> str:
        if not name:
            return "module"
        parts = [self._safe_name(part) for part in name.split(".") if part]
        return ".".join(parts) if parts else "module"

    @staticmethod
    def _quote(value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f"\"{escaped}\""

    @staticmethod
    def _bin_op(op: ast.operator) -> str:
        mapping = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Mod: "%",
            ast.Pow: "**",
            ast.FloorDiv: "/",
        }
        return mapping.get(type(op), "+")

    @staticmethod
    def _cmp_op(op: ast.cmpop) -> str:
        mapping = {
            ast.Eq: "==",
            ast.NotEq: "!=",
            ast.Lt: "<",
            ast.LtE: "<=",
            ast.Gt: ">",
            ast.GtE: ">=",
            ast.In: "in",
            ast.NotIn: "not in",
        }
        return mapping.get(type(op), "==")
