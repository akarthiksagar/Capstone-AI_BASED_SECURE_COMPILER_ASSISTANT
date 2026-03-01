class ASTVisitor:

    def generic_visit(self, node):
        for attr in vars(node).values():
            if isinstance(attr, list):
                for item in attr:
                    if hasattr(item, "accept"):
                        item.accept(self)
            elif hasattr(attr, "accept"):
                attr.accept(self)