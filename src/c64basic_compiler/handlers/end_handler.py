# c64basic_compiler/handlers/end_handler.py

from c64basic_compiler.common.opcodes_6502 import BRK
from c64basic_compiler.handlers.instruction_handler import (
    InstructionHandler,
)


class EndHandler(InstructionHandler):
    def size(self) -> int:
        # END only generates a BRK: 1 byte
        return 1

    def emit(self) -> bytearray:
        machine_code = bytearray()
        machine_code.append(BRK)
        return machine_code
