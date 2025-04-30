# c64basic_compiler/handlers/end_handler.py

from c64basic_compiler.common.opcodes_6502 import BRK, JMP_ABSOLUTE
from c64basic_compiler.handlers.instruction_handler import InstructionHandler


class EndHandler(InstructionHandler):
    def size(self) -> int:
        # BRK (1 byte) + JMP (3 bytes)
        return 4

    def emit(self) -> bytearray:
        if self.current_address is None:
            raise ValueError("current_address must be set before emit() is called.")

        machine_code = bytearray()

        # Emit BRK (software break, optional)
        machine_code.append(BRK)

        # Emit JMP to self.current_address (infinite loop)
        machine_code.append(JMP_ABSOLUTE)
        machine_code.append(self.current_address & 0xFF)
        machine_code.append((self.current_address >> 8) & 0xFF)

        return machine_code






# ----------------------------------------------------------------------------------
# OLD CODE (deprecated)

# c64basic_compiler/handlers/end_handler.py

# from c64basic_compiler.common.opcodes_6502 import BRK
# from c64basic_compiler.handlers.instruction_handler import (
#     InstructionHandler,
# )


# class EndHandler(InstructionHandler):
#     def size(self) -> int:
#         # END only generates a BRK: 1 byte
#         return 1

#     def emit(self) -> bytearray:
#         machine_code = bytearray()
#         machine_code.append(BRK)
#         return machine_code
