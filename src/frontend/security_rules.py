# Static values to verify whether front-end is working or not

DANGEROUS_FUNCTIONS ={

"eval":{
"severity":"HIGH",
"description":"Code Injection: eval() executes arbitrary code.",
"recommendation":"Avoid eval(); use safe parsing (e.g. ast.literal_eval) or explicit logic."
},
"exec":{
"severity":"HIGH",
"description":"Code Injection: exec() executes arbitrary code.",
"recommendation":"Avoid exec(); use direct function calls or dynamic dispatch lookup tables."
},


"os.system":{
"severity":"HIGH",
"description":"Command Injection: os.system() executes shell commands.",
"recommendation":"Use subprocess.run(..., shell=False) instead."
},
"subprocess.call":{
"severity":"MEDIUM",
"description":"Potential Command Injection: subprocess.call with shell=True is dangerous.",
"recommendation":"Ensure shell=False (default) is used."
},
"subprocess.Popen":{
"severity":"MEDIUM",
"description":"Potential Command Injection during process creation.",
"recommendation":"Ensure shell=False is used."
},


"execute":{
"severity":"MEDIUM",
"description":"Potential SQL Injection: Check if raw strings are used in queries.",
"recommendation":"Use parameterized queries (e.g. execute(query, params))."
},


"md5":{
"severity":"MEDIUM",
"description":"Weak Hashing: MD5 is broken and collision-prone.",
"recommendation":"Use SHA-256 or stronger (hashlib.sha256)."
},
"sha1":{
"severity":"MEDIUM",
"description":"Weak Hashing: SHA-1 is vulnerable to collision attacks.",
"recommendation":"Use SHA-256 or stronger."
},
"random":{
"severity":"LOW",
"description":"Predictable Randomness: Not suitable for security/crypto.",
"recommendation":"Use the 'secrets' module for cryptographically strong random numbers."
},
"pickle.load":{
"severity":"HIGH",
"description":"Insecure Deserialization: pickle.load() can execute arbitrary code.",
"recommendation":"Avoid pickling untrusted data; use JSON or other safe formats."
},
"yaml.load":{
"severity":"HIGH",
"description":"Insecure Deserialization: yaml.load() is unsafe by default.",
"recommendation":"Use yaml.safe_load()."
},


"open":{
"severity":"LOW",
"description":"Potential Path Traversal: Opening files with user input.",
"recommendation":"Validate paths using os.path.abspath and check against allowed directories."
}
}
