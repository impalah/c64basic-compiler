# c64basic_compiler/handlers/end_handler.py

from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class EndHandler(InstructionHandler):
    def pseudocode(self) -> list[str]:
        # Pseudocode for END could be a no-operation (NOP) or a RTS
        # depending on the context of the program.
        logger.debug("Generating pseudocode for END instruction")
        return ["END"]
