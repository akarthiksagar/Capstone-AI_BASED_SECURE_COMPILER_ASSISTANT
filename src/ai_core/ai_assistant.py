import random 

class AIAssistant :
    def __init__ (self ):
        self .knowledge_base ={
        "eval":{
        "why":"The 'eval' function executes arbitrary strings as code. If an attacker controls the string, they can run commands on your server.",
        "fix":"Use 'ast.literal_eval' for safe evaluation of literals, or refactor to avoid dynamic code execution entirely."
        },
        "exec":{
        "why":"The 'exec' function allows dynamic execution of Python code, presenting severe security risks including Code Injection.",
        "fix":"Avoid 'exec'. Use a command pattern or a lookup dictionary to execute specific, pre-defined functions."
        },
        "os.system":{
        "why":"Using 'os.system' with user input allows Command Injection (e.g., adding '; rm -rf /').",
        "fix":"Use 'subprocess.run(..., shell=False)' and pass arguments as a list to avoid shell interpretation."
        },
        "md5":{
        "why":"MD5 is a broken hashing algorithm vulnerable to collision attacks.",
        "fix":"Use 'hashlib.sha256()' or 'hashlib.sha512()' for secure hashing."
        },
        "generic":{
        "why":"This pattern matches a known security vulnerability.",
        "fix":"Review the code and apply standard security best practices."
        }
        }

    def explain_vulnerability (self ,vuln_type ):

        key =vuln_type 

        data =self .knowledge_base .get (key )

        if not data and "."in key :

            suffix =key .split (".")[-1 ]

            pass 

        if not data :
            data =self .knowledge_base ["generic"]


        intros =["AI Analysis: ","Security Assistant: ","DeepMind SecureCoder: "]
        intro =random .choice (intros )

        return {
        "explanation":f"{intro }{data ['why']}",
        "suggested_fix":f"Suggested Fix: {data ['fix']}"
        }
