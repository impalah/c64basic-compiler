# c64basic_compiler/handlers/print_handler.py

from c64basic_compiler.handlers.instruction_handler import (
    InstructionHandler,
)
import c64basic_compiler.common.opcodes_6502 as opcodes
import c64basic_compiler.common.kernal_routines as kernal
from c64basic_compiler.common.petscii_map import PETSCII_CONTROL
from c64basic_compiler.utils.print_utils import parse_print_args
from c64basic_compiler.utils.logging import logger


BASE_VARIABLES_ADDR = 0xC000


class PrintHandler(InstructionHandler):

    def pseudocode(self) -> list[str]:
        logger.debug("Generating pseudocode for PRINT instruction")
        args = self.instr["args"]
        output = []
        for arg in args:
            output.append(f"PUSH_CONST {arg}")
            output.append("PRINT")
        return output
