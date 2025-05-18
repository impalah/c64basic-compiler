# c64basic_compiler/handlers/goto_handler.py

from c64basic_compiler.common.opcodes_6502 import JMP_ABSOLUTE
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class GotoHandler(InstructionHandler):

    def pseudocode(self) -> list[str]:
        target_line = int(self.instr["args"][0])
        logger.debug(f"Generating pseudocode for GOTO instruction: GOTO {target_line}")
        return [f"JMP label_{target_line}"]
