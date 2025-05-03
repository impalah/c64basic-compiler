# c64basic_compiler/common/symbol_table.py


class SymbolTable:
    """
    Symbol table for variables used in BASIC.
    Stores name, offset, and type (number/string).
    """

    def __init__(self, base_address=0xC000):
        self.table = {}
        self.offset = 0
        self.base_address = base_address

    def _normalize_name(self, name: str) -> str:
        """
        Normalize variable name to uppercase characters (C64 rule).

        """
        # TODO: probably unnecessary, but keep it for now
        # varname is normalized on LET handler

        # return name.upper()[:2]
        return name.upper()

    def register(
        self,
        name: str,
        size: int,
        vtype: str = "number",
    ) -> int:
        """
        Register a variable if it doesn't exist. Returns absolute address.
        """

        name = self._normalize_name(name)
        if name not in self.table:
            self.table[name] = {
                "offset": self.offset,
                "type": vtype,
            }
            # Update offset for the next variable
            self.offset += size
        return self.get_address(name)

    def get_address(self, name: str) -> int:
        """
        Returns the absolute memory address of a registered variable.
        """
        name = self._normalize_name(name)
        if name not in self.table:
            raise KeyError(f"Variable '{name}' is not defined.")
        return self.base_address + self.table[name]["offset"]

    def get_type(self, name: str) -> str:
        """
        Returns the type of a variable.
        """
        name = self._normalize_name(name)
        return self.table[name]["type"]

    def __contains__(self, name: str) -> bool:
        return self._normalize_name(name) in self.table

    def __repr__(self):
        return f"<SymbolTable base={hex(self.base_address)} vars={list(self.table.keys())}>"
