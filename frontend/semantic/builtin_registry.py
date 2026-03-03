from frontend.semantic.type_system import Type
from frontend.semantic.security_label import SecurityLabel, SecurityLevel


class BuiltinRegistry:

    @staticmethod
    def handle_builtin(name, args):

        if name == "input":
            return Type.STRING, SecurityLabel(SecurityLevel.UNTRUSTED, origin="input")

        if name == "sanitize":
            if not args:
                return Type.NONE, SecurityLabel(SecurityLevel.TAINTED)

            return args[0].type, SecurityLabel(SecurityLevel.SANITIZED, origin="sanitize")

        if name == "len":
            return Type.INT, SecurityLabel(SecurityLevel.TRUSTED)
        
        if name=="exec":
            return Type.NONE,SecurityLabel(SecurityLevel.TRUSTED)
        return None