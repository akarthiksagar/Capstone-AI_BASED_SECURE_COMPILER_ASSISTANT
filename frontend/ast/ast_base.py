class ASTNode:
    """
    Base class for all AST nodes.
    Provides:
        - Source position
        - Parent tracking
        - Semantic annotations
    """

    def __init__(self, line, column):
        self.line = line
        self.column = column
        self.parent = None

        # Will be filled during semantic phase
        self.type = None
        self.security_label = None

    def set_parent(self, parent):
        self.parent = parent

    def accept(self, visitor):
        """
        Visitor pattern entry point.
        """
        method_name = f"visit_{self.__class__.__name__}"
        visitor_fn = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_fn(self)