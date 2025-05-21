# c64basic_compiler/common/compile_context.py

import json

from c64basic_compiler.common.string_area import StringAreaAllocator
from c64basic_compiler.common.symbol_table import SymbolTable


class CompileContext:
    """
    Holds global compilation state for the current program.
    """

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.label_counter = 0
        self.loop_stack = []
        self.string_area = StringAreaAllocator()

    def new_label(self, prefix="L") -> str:
        """
        Generate a new unique label (for IF, FOR, etc.).
        """
        label = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return label

    def to_dict(self) -> dict:
        """
        Convert the CompileContext instance to a dictionary for serialization.
        """
        return {
            "symbol_table": repr(
                self.symbol_table
            ),  # Assuming SymbolTable has a __repr__ method
            "label_counter": self.label_counter,
            "loop_stack": self.loop_stack,
            "string_area": repr(
                self.string_area
            ),  # Assuming StringAreaAllocator has a __repr__ method
        }

    def __repr__(self) -> str:
        """
        Return a JSON-formatted string representation of the CompileContext.
        """
        return json.dumps(self.to_dict(), indent=4)
