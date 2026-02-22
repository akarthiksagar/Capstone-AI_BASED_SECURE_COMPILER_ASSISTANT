from typing import List, Dict, Set, Optional
from dataclasses import dataclass, field
import re

from .ast_nodes import (
    ASTVisitor, ASTNode, Program, FunctionDef, Call, MemberAccess,
    Identifier, Assignment, ExpressionStatement, If, While, For,
    Return, Import, BinaryOp, StringLiteral
)
from ..utils.errors import SecurityIssue, Severity


@dataclass
class DangerousPattern:
    name: str
    severity: Severity
    description: str
    recommendation: str
    cwe_id: Optional[str] = None
    patterns: List[str] = field(default_factory=list)


SECURITY_PATTERNS: Dict[str, DangerousPattern] = {
    'eval': DangerousPattern(
        name='eval',
        severity=Severity.CRITICAL,
        description='Code Injection: eval() executes arbitrary Python code, allowing attackers to run malicious commands.',
        recommendation='Use ast.literal_eval() for safe literal evaluation, or implement explicit parsing logic.',
        cwe_id='CWE-94',
        patterns=['eval']
    ),
    'exec': DangerousPattern(
        name='exec',
        severity=Severity.CRITICAL,
        description='Code Injection: exec() executes arbitrary Python code, enabling complete system compromise.',
        recommendation='Avoid exec() entirely. Use safe alternatives like predefined functions or sandboxed execution.',
        cwe_id='CWE-94',
        patterns=['exec']
    ),
    'compile': DangerousPattern(
        name='compile',
        severity=Severity.HIGH,
        description='Code Compilation: compile() creates code objects that can be executed, potentially from untrusted input.',
        recommendation='Avoid compile() with user input. Use static analysis or sandboxed environments instead.',
        cwe_id='CWE-94',
        patterns=['compile']
    ),
    'os.system': DangerousPattern(
        name='os.system',
        severity=Severity.CRITICAL,
        description='Command Injection: os.system() executes shell commands, vulnerable to injection attacks.',
        recommendation='Use subprocess.run() with shell=False and pass arguments as a list.',
        cwe_id='CWE-78',
        patterns=['system']
    ),
    'os.popen': DangerousPattern(
        name='os.popen',
        severity=Severity.CRITICAL,
        description='Command Injection: os.popen() executes shell commands with output capture.',
        recommendation='Use subprocess.run() with shell=False for safer command execution.',
        cwe_id='CWE-78',
        patterns=['popen']
    ),
    'subprocess.shell': DangerousPattern(
        name='subprocess with shell=True',
        severity=Severity.HIGH,
        description='Command Injection: subprocess with shell=True is vulnerable to shell injection.',
        recommendation='Use shell=False and pass command as a list of arguments.',
        cwe_id='CWE-78',
        patterns=['call', 'run', 'Popen', 'check_output', 'check_call']
    ),
    'pickle.loads': DangerousPattern(
        name='pickle.loads',
        severity=Severity.CRITICAL,
        description='Insecure Deserialization: pickle.loads() can execute arbitrary code during deserialization.',
        recommendation='Use JSON or other safe serialization formats. Never unpickle untrusted data.',
        cwe_id='CWE-502',
        patterns=['loads', 'load']
    ),
    'yaml.load': DangerousPattern(
        name='yaml.load',
        severity=Severity.HIGH,
        description='Insecure Deserialization: yaml.load() without safe_load can execute arbitrary code.',
        recommendation='Use yaml.safe_load() instead of yaml.load().',
        cwe_id='CWE-502',
        patterns=['load']
    ),
    'sql_injection': DangerousPattern(
        name='SQL Injection',
        severity=Severity.CRITICAL,
        description='SQL Injection: String concatenation in SQL queries allows injection attacks.',
        recommendation='Use parameterized queries or prepared statements.',
        cwe_id='CWE-89',
        patterns=['execute', 'executemany']
    ),
    'file_operations': DangerousPattern(
        name='Unsafe File Operations',
        severity=Severity.MEDIUM,
        description='File Operations: open() with user-controlled paths may lead to path traversal.',
        recommendation='Validate and sanitize file paths. Use os.path.realpath() to resolve paths.',
        cwe_id='CWE-22',
        patterns=['open']
    ),
}


DANGEROUS_MODULES: Dict[str, List[str]] = {
    'os': ['system', 'popen', 'spawn', 'exec'],
    'subprocess': ['call', 'run', 'Popen', 'check_output', 'check_call'],
    'pickle': ['loads', 'load', 'Unpickler'],
    'marshal': ['loads', 'load'],
    'shelve': ['open'],
    'yaml': ['load', 'unsafe_load'],
    'commands': ['getoutput', 'getstatusoutput'],
}


class SecurityWalker(ASTVisitor):

    def __init__(self):
        self.issues: List[SecurityIssue] = []
        self.imported_modules: Set[str] = set()
        self.dangerous_aliases: Dict[str, str] = {}
        self.string_variables: Dict[str, str] = {}

    def analyze(self, ast: Program) -> List[SecurityIssue]:
        self.issues = []
        self.imported_modules = set()
        self.dangerous_aliases = {}
        self.string_variables = {}
        self.visit(ast)
        return self.issues

    def _add_issue(self, name: str, line: int, column: int, pattern: DangerousPattern) -> None:
        issue = SecurityIssue(
            name=name,
            severity=pattern.severity,
            line=line,
            column=column,
            description=pattern.description,
            recommendation=pattern.recommendation,
            cwe_id=pattern.cwe_id,
            phase="Frontend"
        )
        self.issues.append(issue)

    def _check_function_call(self, func_name: str, line: int, column: int, module: Optional[str] = None) -> None:
        if func_name in SECURITY_PATTERNS:
            self._add_issue(func_name, line, column, SECURITY_PATTERNS[func_name])
            return

        if module:
            full_name = f"{module}.{func_name}"
            if module in DANGEROUS_MODULES:
                if func_name in DANGEROUS_MODULES[module]:
                    for pattern_key, pattern in SECURITY_PATTERNS.items():
                        if func_name in pattern.patterns and module in pattern_key:
                            self._add_issue(full_name, line, column, pattern)
                            return
                    if module == 'pickle' and func_name in ['loads', 'load']:
                        self._add_issue(full_name, line, column, SECURITY_PATTERNS['pickle.loads'])
                    elif module == 'os' and func_name == 'system':
                        self._add_issue(full_name, line, column, SECURITY_PATTERNS['os.system'])
                    elif module == 'subprocess':
                        self._add_issue(full_name, line, column, SECURITY_PATTERNS['subprocess.shell'])

    def visit_program(self, node: Program) -> None:
        for stmt in node.statements:
            self.visit(stmt)

    def visit_import(self, node: Import) -> None:
        self.imported_modules.add(node.module)

    def visit_function_def(self, node: FunctionDef) -> None:
        for stmt in node.body:
            self.visit(stmt)

    def visit_assignment(self, node: Assignment) -> None:
        if isinstance(node.target, Identifier) and isinstance(node.value, StringLiteral):
            self.string_variables[node.target.name] = node.value.value
        self.visit(node.value)

    def visit_expression_statement(self, node: ExpressionStatement) -> None:
        self.visit(node.expression)

    def visit_call(self, node: Call) -> None:
        line = node.line
        column = node.column

        if isinstance(node.function, Identifier):
            func_name = node.function.name
            self._check_function_call(func_name, line, column)

        elif isinstance(node.function, MemberAccess):
            member_access = node.function
            func_name = member_access.member

            if isinstance(member_access.object, Identifier):
                module_name = member_access.object.name
                self._check_function_call(func_name, line, column, module_name)

            if func_name in ['call', 'run', 'Popen', 'check_output', 'check_call']:
                for key, value in node.keyword_args.items():
                    if key == 'shell':
                        self._add_issue(
                            f"subprocess.{func_name} with shell argument",
                            line, column,
                            SECURITY_PATTERNS['subprocess.shell']
                        )
                        break

        for arg in node.arguments:
            self.visit(arg)

    def visit_if(self, node: If) -> None:
        self.visit(node.condition)
        for stmt in node.then_body:
            self.visit(stmt)
        for stmt in node.else_body:
            self.visit(stmt)

    def visit_while(self, node: While) -> None:
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)

    def visit_for(self, node: For) -> None:
        self.visit(node.iterable)
        for stmt in node.body:
            self.visit(stmt)

    def visit_return(self, node: Return) -> None:
        if node.value:
            self.visit(node.value)

    def visit_binary_op(self, node: BinaryOp) -> None:
        self.visit(node.left)
        self.visit(node.right)

    def visit_member_access(self, node: MemberAccess) -> None:
        self.visit(node.object)

    def visit_identifier(self, node: Identifier) -> None:
        pass

    def visit_number(self, node) -> None:
        pass

    def visit_string(self, node: StringLiteral) -> None:
        pass

    def visit_boolean(self, node) -> None:
        pass

    def visit_none(self, node) -> None:
        pass

    def visit_list(self, node) -> None:
        for elem in node.elements:
            self.visit(elem)

    def visit_dict(self, node) -> None:
        for key, value in node.entries:
            self.visit(key)
            self.visit(value)

    def visit_unary_op(self, node) -> None:
        self.visit(node.operand)

    def visit_subscript(self, node) -> None:
        self.visit(node.object)
        self.visit(node.index)
