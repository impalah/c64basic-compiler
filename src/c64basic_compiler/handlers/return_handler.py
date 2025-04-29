# c64basic_compiler/handlers/return_handler.py

from c64basic_compiler.common.opcodes_6502 import RTS
from c64basic_compiler.handlers.instruction_handler import InstructionHandler

class ReturnHandler(InstructionHandler):
    def size(self) -> int:
        # RETURN genera un solo RTS
        return 1

    def emit(self) -> bytearray:
        machine_code = bytearray()
        machine_code.append(RTS)
        return machine_code
