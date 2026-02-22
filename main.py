
import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.frontend.lexer_parser import Frontend
from src.frontend.ast_nodes import ASTPrinter
from src.middle_end.ir_generator import IRGenerator
from src.middle_end.ir import IRProgram, IRInstruction
from src.middle_end.security_analyzer import MiddleEndSecurityAnalyzer
from src.utils.errors import CompilationResult, Severity
from src.utils.logger import logger


def print_banner():
    print("-" * 60)
    print("   Capstone - Secure Compiler Assistant")
    print("   Mode: Frontend -> IR Analysis")
    print("-" * 60)


def read_source_file(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def get_vulnerable_lines(security_issues: list) -> dict:
    vulnerable_lines = {}
    for issue in security_issues:
        line = issue.line
        if line not in vulnerable_lines:
            vulnerable_lines[line] = []
        vulnerable_lines[line].append(issue)
    return vulnerable_lines


def print_vulnerable_ir(ir_program: IRProgram, security_issues: list):
    vulnerable_lines = get_vulnerable_lines(security_issues)

    print("\n=== VULNERABLE IR ANALYSIS ===\n")

    if ir_program.global_instructions:
        print("Global Instructions:")
        _print_instructions_with_vulnerabilities(
            ir_program.global_instructions,
            vulnerable_lines
        )

    for func in ir_program.functions:
        print(f"\nFunction: {func.name}({', '.join(func.parameters)})")
        print("-" * 40)
        _print_instructions_with_vulnerabilities(
            func.instructions,
            vulnerable_lines
        )


def _print_instructions_with_vulnerabilities(instructions: list, vulnerable_lines: dict):
    RED = "\033[91m"
    RESET = "\033[0m"

    for instr in instructions:
        line_num = instr.line
        instr_str = str(instr)

        if line_num in vulnerable_lines:
            issues = vulnerable_lines[line_num]
            print(f"{RED}>>> {instr_str}{RESET}")

            for issue in issues:
                print(f"      {RED}[{issue.severity.value}] {issue.name}{RESET}")
                print(f"      Description: {issue.description}")
                if issue.cwe_id:
                    print(f"      CWE: {issue.cwe_id}")
        else:
            print(f"    {instr_str}")


def print_clean_ir(ir_program: IRProgram):
    print("\n=== CLEAN IR OUTPUT ===\n")
    print(str(ir_program))


def compile_source(source: str, filepath: str, args) -> tuple:
    result = CompilationResult(success=True)
    ir_program = None

    logger.phase_start("Phase 1: Frontend Analysis")

    frontend = Frontend()
    frontend_result = frontend.process(source)
    result.merge(frontend_result)

    if frontend_result.has_errors():
        logger.phase_complete("Frontend", success=False)
        return result, None

    if frontend_result.security_issues:
        print(f"Frontend detected {len(frontend_result.security_issues)} security issue(s)")

    logger.phase_complete("Frontend", success=True)

    ast = frontend.get_ast()

    if args.print_ast:
        print("\n=== AST Structure ===")
        printer = ASTPrinter()
        printer.visit(ast)

    logger.phase_start("Phase 2: IR Generation & Security Analysis")

    ir_generator = IRGenerator()
    ir_program = ir_generator.generate(ast)

    me_analyzer = MiddleEndSecurityAnalyzer()
    me_result = me_analyzer.analyze(ir_program)
    result.merge(me_result)

    if me_result.security_issues:
        print(f"Middle-End detected {len(me_result.security_issues)} security issue(s)")

    logger.phase_complete("Middle-End", success=True)

    if args.print_ir:
        if result.security_issues:
            print_vulnerable_ir(ir_program, result.security_issues)
        else:
            print_clean_ir(ir_program)
    else:
        if result.security_issues:
            print(f"\n{len(result.security_issues)} security issues detected. Use --print-ir to see details.")

    return result, ir_program


def main():
    parser = argparse.ArgumentParser(
        description="Capstone - Secure Compiler Assistant (Simplified Mode)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py sample_programs/vulnerable.src --print-ir
    python main.py sample_programs/safe.src --print-ast --print-ir
        """
    )

    parser.add_argument(
        'source_file',
        help='Source file to compile (.src)'
    )

    parser.add_argument(
        '--print-ast',
        action='store_true',
        help='Print the Abstract Syntax Tree'
    )

    parser.add_argument(
        '--print-ir',
        action='store_true',
        help='Print the Intermediate Representation with vulnerability annotations'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output report in JSON format'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    print_banner()

    print(f"Compiling: {args.source_file}")
    source = read_source_file(args.source_file)

    result, ir_program = compile_source(source, args.source_file, args)

    if args.json:
        import json
        report_data = {
            "file": args.source_file,
            "success": result.success,
            "security_issues": [
                {
                    "line": i.line,
                    "severity": i.severity.value,
                    "name": i.name,
                    "description": i.description,
                    "cwe_id": i.cwe_id,
                    "recommendation": i.recommendation
                }
                for i in result.security_issues
            ],
            "ir_generated": ir_program is not None
        }
        print(json.dumps(report_data, indent=2))
    else:
        logger.print_security_report(result.security_issues)
        logger.print_summary(result)

    if result.has_errors():
        sys.exit(2)
    elif any(i.severity in [Severity.CRITICAL, Severity.HIGH] for i in result.security_issues):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
