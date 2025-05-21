from c64basic_compiler.common.compile_context import CompileContext


class InstructionHandler:
    """Base class for handling instructions in the C64 BASIC compiler."""

    def __init__(self, instr: str, context: CompileContext):
        self.instr = instr
        self.context: CompileContext = context  # line_addresses, symbol_table, etc.
        self.current_address: int | None = None  # Set externally in generate_code()

    # def size(self) -> int:
    #     """Calculate the size of the instruction in bytes.

    #     Raises:
    #         NotImplementedError: _description_

    #     Returns:
    #         int: _description_
    #     """
    #     raise NotImplementedError

    # def emit(self) -> bytearray:
    #     """Generate the machine code for the instruction.

    #     Raises:
    #         NotImplementedError: _description_

    #     Returns:
    #         bytearray: _description_
    #     """

    #     raise NotImplementedError

    def pseudocode(self) -> list[str]:
        """Generate the pseudocode for the instruction.

        Raises:
            NotImplementedError: _description_

        Returns:
            str: _description_
        """
        raise NotImplementedError
