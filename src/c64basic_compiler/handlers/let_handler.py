# c64basic_compiler/handlers/let_handler.py

from typing import Any
import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger

# TODO: Make configurable
# Base address for string area in memory
BASE_VARIABLES_ADDR = 0xC000


class LetHandler(InstructionHandler):
    """Manages the LET instruction in C64 BASIC.

    Args:
        InstructionHandler (_type_): _description_
    """

    def pseudocode(self) -> list[str]:
        """Generate pseudocode for the LET instruction.

        Returns:
            str: _description_
        """

        # TODO: Implementar la generación de pseudocódigo para LET
        # This is a simple implementation. You may want to improve it.

        varname = self.instr["args"][0]
        value_token = self.instr["args"][2]
        logger.debug(
            f"** Generating pseudocode for LET instruction: {varname} = {value_token}"
        )
        return [f"{varname} = {value_token}"]
