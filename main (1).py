import sys
import os
import argparse

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'frontend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'middle_end'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'ai_core'))

from antlr4 import *
from src.frontend.PythonAssistantLexer import PythonAssistantLexer
from src.frontend.PythonAssistantParser import PythonAssistantParser
from src.frontend.security_walker import SecurityWalker
from src.frontend.semantic_analyzer import SemanticAnalyzer
from src.ai_core.ai_assistant import AIAssistant

def compile_source(input_file):
    print(f"Compiling {input_file}...")
    
    try:
        input_stream = FileStream(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 1. Lexing
    lexer = PythonAssistantLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    
    # 2. Parsing
    parser = PythonAssistantParser(token_stream)
    parser.removeErrorListeners() # Use custom listener if needed, or default to console
    tree = parser.file_input()
    
    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"Syntax Errors: {parser.getNumberOfSyntaxErrors()}")
        return

    # 3. Semantic Analysis
    print("Running Semantic Analysis...")
    semantic_analyzer = SemanticAnalyzer()
    walker = ParseTreeWalker()
    walker.walk(semantic_analyzer, tree)
    
    if semantic_analyzer.errors:
        print("\n[Semantic Errors]")
        for err in semantic_analyzer.errors:
            print(f"  Line {err['line']}: {err['message']}")
    else:
        print("  > Semantic checks passed.")

    # 4. Security Analysis
    print("Running Security Analysis...")
    security_walker = SecurityWalker(token_stream)
    walker.walk(security_walker, tree)
    
    issues = security_walker.issues
    if issues:
        print(f"\n[Security Issues Found: {len(issues)}]")
        
        # Initialize AI Assistant
        try:
             ai_agent = AIAssistant()
        except:
             ai_agent = None
             print("Warning: AI Assistant could not be initialized.")

        for i, issue in enumerate(issues, 1):
            print(f"\n  #{i} {issue['function']} (Severity: {issue['severity']})")
            print(f"     Line: {issue['line']}")
            print(f"     Description: {issue['description']}")
            print(f"     Recommendation: {issue['recommendation']}")
            
            if ai_agent:
                try:
                    insight = ai_agent.explain_vulnerability(issue['function'])
                    print(f"     [AI Insight]: {insight.get('explanation', 'No explanation')}")
                    print(f"     [AI Fix]: {insight.get('suggested_fix', 'No fix')}")
                except Exception as e:
                    print(f"     [AI Error]: {e}")
    else:
        print("  > No security issues found.")

def main():
    parser = argparse.ArgumentParser(description="AI-Based Secure Compiler Assistant")
    parser.add_argument("input_file", nargs='?', default="user_code.py", help="Source code file to compile")
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        print("Creating a default 'user_code.py' for you...")
        create_default_user_code(args.input_file)
        
    compile_source(args.input_file)

def create_default_user_code(filename):
    code = """def main(): {
    x = 10
    print(x)
    
    # Secure code
    s = "hello"
    
    # Insecure code examples
    os.system("rm -rf /")
    eval("2 + 2")
}

main()
"""
    with open(filename, "w") as f:
        f.write(code)
    print(f"Created {filename}")

if __name__ == '__main__':
    main()