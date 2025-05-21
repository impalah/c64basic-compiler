# c64basic_compiler/handlers/return_handler.py

from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class ReturnHandler(InstructionHandler):
    def pseudocode(self) -> list[str]:
        logger.debug("Generating pseudocode for RETURN instruction")
        return ["RET"]
