# c64basic_compiler/handlers/rem_handler.py

from c64basic_compiler.handlers.instruction_handler import InstructionHandler


class RemHandler(InstructionHandler):
    def size(self) -> int:
        # REM does not generate any machine code
        # It is just a comment and does not affect the program
        return 0

    def emit(self) -> bytearray:
        # REM does not generate any machine code
        return bytearray()
