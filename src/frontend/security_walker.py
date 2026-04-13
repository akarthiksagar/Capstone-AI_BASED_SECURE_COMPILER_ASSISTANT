from .PythonAssistantParserListener import PythonAssistantParserListener 
from .security_rules import DANGEROUS_FUNCTIONS 

class SecurityWalker (PythonAssistantParserListener ):
    def __init__ (self ,token_stream =None ):
        self .issues =[]
        self .token_stream =token_stream 

    def enterFactor(self, ctx):
        # factor: atom trailer*
        
        # We only care if the atom is an ID (e.g., 'os' or 'eval')
        if not ctx.atom().ID():
            return
            
        atom_text = ctx.atom().ID().getText()
        full_name = atom_text
        
        # Check trailers for attribute access (e.g. .system)
        # trailer: LPAREN arglist? RPAREN | DOT ID
        if ctx.trailer():
            for trailer in ctx.trailer():
                # We are looking for .name
                # The trailer text will include the dot, e.g. ".system"
                text = trailer.getText()
                if text.startswith('.'):
                    full_name += text
                # We stop accumulating at function calls or other logical boundaries
                # For this assignment, simple concatenation of dots is enough to match "os.system"
                
        # Check if the reconstructed name is dangerous
        if full_name in DANGEROUS_FUNCTIONS:
            self._add_issue(full_name, ctx.start.line)

    def _add_issue(self, func_name, line):
        rule = DANGEROUS_FUNCTIONS[func_name]
        self.issues.append({
            "function": func_name,
            "line": line,
            "severity": rule["severity"],
            "description": rule["description"],
            "recommendation": rule["recommendation"]
        })
