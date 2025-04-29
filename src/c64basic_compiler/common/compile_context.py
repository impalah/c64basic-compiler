# c64basic_compiler/common/compile_context.py

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
