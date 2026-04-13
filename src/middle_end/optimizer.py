from src .frontend .PythonAssistantParserListener import PythonAssistantParserListener 
from src .frontend .security_rules import DANGEROUS_FUNCTIONS 

class SecurityOptimizer (PythonAssistantParserListener ):
    def __init__ (self ):
        self .constants ={}
        self .issues =[]
        self .current_expr =None 

    def enterAssignment (self ,ctx ):


        pass 

    def exitAssignment (self ,ctx ):

        var_name =ctx .ID ().getText ()



        pass 





    def optimize_and_check (self ,ctx ):


        pass 





class ObfuscationDetector (PythonAssistantParserListener ):
    def __init__ (self ):
        self .issues =[]

    def enterTerm (self ,ctx ):


        pass 

    def enterExpr (self ,ctx ):


        if ctx .children and len (ctx .children )>1 :
            try :

                path_text =self ._extract_string_concat (ctx )
                if path_text :

                   self ._check_danger (path_text ,ctx .start .line )
            except Exception :
                pass 

    def _extract_string_concat (self ,ctx ):


        full_text =""

        raw_text =ctx .getText ()
        if "+"in raw_text and '"'in raw_text :


            parts =raw_text .split ('+')
            reconstructed =""
            for p in parts :
                p =p .strip ()
                if (p .startswith ('"')and p .endswith ('"'))or (p .startswith ("'")and p .endswith ("'")):
                    reconstructed +=p [1 :-1 ]
                else :
                    return None 
            return reconstructed 
        return None 

    def _check_danger (self ,text ,line ):
        if text in DANGEROUS_FUNCTIONS :
             self .issues .append ({
             "function":text ,
             "line":line ,
             "severity":"CRITICAL",
             "description":f"Obfuscated Warning: Detected hidden '{text }' via Constant Folding.",
             "recommendation":"Remove obfuscation and validate logic."
             })
