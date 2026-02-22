"""
Logging utilities for the Capstone Compiler Assistant
Simplified version removing 'rich' dependency.
"""
import sys
from typing import List, Optional
from .errors import SecurityIssue, CompilerError, Severity, CompilationResult


class CompilerLogger:
    """Logger with standard output for compiler"""
    
    # ANSI Color codes
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def info(self, message: str) -> None:
        """Print info message"""
        print(f"{self.BLUE}i{self.RESET} {message}")
    
    def success(self, message: str) -> None:
        """Print success message"""
        print(f"{self.GREEN}✓{self.RESET} {message}")
    
    def warning(self, message: str) -> None:
        """Print warning message"""
        print(f"{self.YELLOW}⚠{self.RESET} {message}")
    
    def error(self, message: str) -> None:
        """Print error message"""
        print(f"{self.RED}✗{self.RESET} {message}")
    
    def phase_start(self, phase_name: str) -> None:
        """Indicate start of a compilation phase"""
        print(f"\n{self.CYAN}{self.BOLD}=== {phase_name} ==={self.RESET}")
    
    def phase_complete(self, phase_name: str, success: bool = True) -> None:
        """Indicate completion of a compilation phase"""
        if success:
            print(f"{self.GREEN}✓{self.RESET} {phase_name} completed successfully")
        else:
            print(f"{self.RED}✗{self.RESET} {phase_name} completed with errors")
    
    def print_errors(self, errors: List[CompilerError]) -> None:
        """Print a list of compiler errors"""
        if not errors:
            return
        
        print(f"\n{self.RED}{self.BOLD}Compilation Errors:{self.RESET}")
        
        for error in errors:
            print(f"  {self.RED}•{self.RESET} {error}")
    
    def print_security_report(self, issues: List[SecurityIssue]) -> None:
        """Print security issues in a simple list"""
        if not issues:
            print(f"\n{self.GREEN}{self.BOLD}No security issues detected!{self.RESET}")
            return
        
        print(f"\n{self.RED}{self.BOLD}Security Issues Found: {len(issues)}{self.RESET}")
        
        # Group by severity
        critical = [i for i in issues if i.severity == Severity.CRITICAL]
        high = [i for i in issues if i.severity == Severity.HIGH]
        medium = [i for i in issues if i.severity == Severity.MEDIUM]
        low = [i for i in issues if i.severity == Severity.LOW]
        
        severity_groups = [
            ("CRITICAL", critical, self.RED),
            ("HIGH", high, self.RED),
            ("MEDIUM", medium, self.YELLOW),
            ("LOW", low, self.BLUE),
        ]
        
        for severity_name, group, color in severity_groups:
            if group:
                print(f"\n{color}▸ {severity_name} ({len(group)}){self.RESET}")
                for issue in group:
                    print(f"  {color}#{issue.line}{self.RESET} {issue.name}")
                    print(f"      {self.DIM}{issue.description}{self.RESET}")
                    print(f"      → {issue.recommendation}")
    
    def print_summary(self, result: CompilationResult) -> None:
        """Print final compilation summary"""
        print(f"\n{self.BOLD}Compilation Summary{self.RESET}")
        print("-" * 30)
        
        status = f"{self.GREEN}SUCCESS{self.RESET}" if result.success else f"{self.RED}FAILED{self.RESET}"
        print(f"Status          : {status}")
        print(f"Errors          : {len(result.errors)}")
        print(f"Security Issues : {len(result.security_issues)}")
        print("-" * 30)
    
    def print_source_context(self, source: str, line: int, message: str) -> None:
        """Print source code with highlighted line"""
        lines = source.split('\n')
        start = max(0, line - 2)
        end = min(len(lines), line + 2)
        
        for i in range(start, end):
            line_num = i + 1
            if line_num == line:
                print(f"  {self.RED}→ {line_num:4d} | {lines[i]}{self.RESET}")
            else:
                print(f"    {line_num:4d} | {lines[i]}")
        
        print(f"       {self.RED}{message}{self.RESET}")


# Global logger instance
logger = CompilerLogger()
