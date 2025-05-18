# c64basic_compiler/handlers/gosub_handler.py

from c64basic_compiler.common.opcodes_6502 import JSR_ABSOLUTE
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class GosubHandler(InstructionHandler):

    def pseudocode(self) -> list[str]:
        target_line = int(self.instr["args"][0])
        logger.debug(
            f"Generating pseudocode for GOSUB instruction: GOSUB {target_line}"
        )
        return [f"CALL label_{target_line}"]
