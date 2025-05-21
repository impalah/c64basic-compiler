# c64basic_compiler/handlers/rem_handler.py

from c64basic_compiler.handlers.instruction_handler import InstructionHandler


class RemHandler(InstructionHandler):
    def pseudocode(self) -> list[str]:
        # Generate pseudocode for REM
        # It is just a comment and does not affect the program
        return [f"REM {' '.join(self.instr['args'])}"]
