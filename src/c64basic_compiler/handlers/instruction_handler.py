from typing import Any


class InstructionHandler:
    """Base class for handling instructions in the C64 BASIC compiler."""

    def __init__(self, instr: str, context):
        self.instr = instr
        self.context = context  # line_addresses, symbol_table, etc.

    def size(self) -> int:
        """Calculate the size of the instruction in bytes.

        Raises:
            NotImplementedError: _description_

        Returns:
            int: _description_
        """
        raise NotImplementedError

    def emit(self) -> bytearray:
        """Generate the machine code for the instruction.

        Raises:
            NotImplementedError: _description_

        Returns:
            bytearray: _description_
        """

        raise NotImplementedError
