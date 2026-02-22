"""
Error classes for the Secure Compiler Assistant
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    """Severity levels for security issues"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class ErrorType(Enum):
    """Types of compiler errors"""
    LEXICAL = "Lexical Error"
    SYNTAX = "Syntax Error"
    SEMANTIC = "Semantic Error"
    SECURITY = "Security Issue"
    INTERNAL = "Internal Error"


@dataclass
class CompilerError:
    """Base class for compiler errors"""
    error_type: ErrorType
    message: str
    line: int
    column: int = 0
    source_line: Optional[str] = None
    
    def __str__(self) -> str:
        location = f"Line {self.line}"
        if self.column > 0:
            location += f", Column {self.column}"
        return f"[{self.error_type.value}] {location}: {self.message}"


@dataclass
class SecurityIssue:
    """Represents a detected security vulnerability"""
    name: str
    severity: Severity
    line: int
    column: int
    description: str
    recommendation: str
    cwe_id: Optional[str] = None
    phase: str = "Frontend"  # Frontend, Middle-End, Backend
    
    def __str__(self) -> str:
        return (
            f"[{self.severity.value}] {self.name}\n"
            f"  Location: Line {self.line}, Column {self.column}\n"
            f"  Phase: {self.phase}\n"
            f"  Description: {self.description}\n"
            f"  Recommendation: {self.recommendation}"
        )


@dataclass
class CompilationResult:
    """Result of a compilation pass"""
    success: bool
    errors: List[CompilerError] = field(default_factory=list)
    security_issues: List[SecurityIssue] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_error(self, error: CompilerError) -> None:
        self.errors.append(error)
        self.success = False
    
    def add_security_issue(self, issue: SecurityIssue) -> None:
        self.security_issues.append(issue)
    
    def has_errors(self) -> bool:
        return len(self.errors) > 0
    
    def has_security_issues(self) -> bool:
        return len(self.security_issues) > 0
    
    def merge(self, other: 'CompilationResult') -> 'CompilationResult':
        """Merge results from another compilation phase"""
        self.errors.extend(other.errors)
        self.security_issues.extend(other.security_issues)
        self.warnings.extend(other.warnings)
        if not other.success:
            self.success = False
        return self
