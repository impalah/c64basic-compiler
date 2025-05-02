# c64basic_compiler/handlers/return_handler.py

from c64basic_compiler.common.opcodes_6502 import RTS
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.utils.logging import logger


class ReturnHandler(InstructionHandler):
    def size(self) -> int:
        # RETURN genera un solo RTS
        logger.debug("Calculating size for RETURN instruction: 1 byte")
        return 1

    def emit(self) -> bytearray:
        machine_code = bytearray()
        machine_code.append(RTS)
        logger.debug(f"Emitting RETURN at address {self.current_address}")
        return machine_code
