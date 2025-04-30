# c64basic_compiler/handlers/end_handler.py

from c64basic_compiler.common.opcodes_6502 import (
    LDA_IMMEDIATE,
    CMP_IMMEDIATE,
    JSR_ABSOLUTE,
    BEQ,
    JMP_ABSOLUTE,
)
from c64basic_compiler.handlers.instruction_handler import InstructionHandler
from c64basic_compiler.common.kernal_routines import CHROUT, GETIN
from c64basic_compiler.common.petscii_map import PETSCII_CONTROL


class EndHandler(InstructionHandler):
    def size(self) -> int:
        # Estimación conservadora
        return 150

    def emit(self) -> bytearray:
        """Prints a message and waits for a key press.

        Raises:
            ValueError: _description_

        Returns:
            bytearray: _description_
        """
        if self.current_address is None:
            raise ValueError("current_address must be set before emit() is called.")

        message = "PRESS ANY KEY TO EXIT"

        machine_code = bytearray()

        # 1. Imprimir el mensaje
        for char in message:
            machine_code.append(LDA_IMMEDIATE)
            machine_code.append(ord(char))
            machine_code.append(JSR_ABSOLUTE)
            machine_code.append(CHROUT & 0xFF)
            machine_code.append((CHROUT >> 8) & 0xFF)

        # CR
        machine_code.append(LDA_IMMEDIATE)
        machine_code.append(PETSCII_CONTROL["CR"])
        machine_code.append(JSR_ABSOLUTE)
        machine_code.append(CHROUT & 0xFF)
        machine_code.append((CHROUT >> 8) & 0xFF)

        # 2. Bucle de espera de tecla
        wait_loop_addr = self.current_address + len(machine_code)

        # JSR GETIN
        machine_code.append(JSR_ABSOLUTE)
        machine_code.append(GETIN & 0xFF)
        machine_code.append((GETIN >> 8) & 0xFF)

        # CMP #$00
        machine_code.append(CMP_IMMEDIATE)
        machine_code.append(0x00)

        # BEQ -7 → vuelve a GETIN
        machine_code.append(BEQ)
        machine_code.append(0xF9)

        # 3. Bucle infinito limpio al final
        halt_addr = self.current_address + len(machine_code)

        machine_code.append(JMP_ABSOLUTE)
        machine_code.append(halt_addr & 0xFF)
        machine_code.append((halt_addr >> 8) & 0xFF)

        return machine_code






# ---------------------------------------------------------------------
# OLD CODE (deprecated): wait for key press

# from c64basic_compiler.common.opcodes_6502 import (
#     LDA_IMMEDIATE,
#     CMP_IMMEDIATE,
#     JSR_ABSOLUTE,
#     BEQ,
#     RTS,
# )
# from c64basic_compiler.handlers.instruction_handler import InstructionHandler
# from c64basic_compiler.utils.logging import logger

# GETIN = 0xFFE4  # KERNAL routine to get a key press (returns 0 if no key)

# class EndHandler(InstructionHandler):
#     def size(self) -> int:
#         # JSR (3) + CMP (2) + BEQ (2) + RTS (1) = 8 bytes total
#         return 8

#     def emit(self) -> bytearray:
#         if self.current_address is None:
#             raise ValueError("current_address must be set before emit() is called.")

#         machine_code = bytearray()

#         # JSR $FFE4  ; GETIN
#         machine_code.append(JSR_ABSOLUTE)
#         machine_code.append(GETIN & 0xFF)
#         machine_code.append((GETIN >> 8) & 0xFF)

#         # CMP #$00
#         machine_code.append(CMP_IMMEDIATE)
#         machine_code.append(0x00)

#         # BEQ .wait_loop (offset to jump back 5 bytes)
#         machine_code.append(BEQ)
#         machine_code.append(0xF9)  # -7 in two's complement (JSR + CMP + BEQ = 7 bytes)

#         # RTS (return to BASIC)
#         machine_code.append(RTS)

#         logger.debug(f"Emitting END (wait for key) at address {self.current_address}")
#         return machine_code



















# ----------------------------------------------------------------------------------
# OLD CODE (deprecated): break + jump to self.current_address

# from c64basic_compiler.common.opcodes_6502 import BRK, JMP_ABSOLUTE
# from c64basic_compiler.handlers.instruction_handler import InstructionHandler
# from c64basic_compiler.utils.logging import logger

# class EndHandler(InstructionHandler):
#     def size(self) -> int:
#         # BRK (1 byte) + JMP (3 bytes)
#         return 4

#     def emit(self) -> bytearray:
#         if self.current_address is None:
#             raise ValueError("current_address must be set before emit() is called.")

#         machine_code = bytearray()

#         # Emit BRK (software break, optional)
#         machine_code.append(BRK)

#         # Emit JMP to self.current_address (infinite loop)
#         machine_code.append(JMP_ABSOLUTE)
#         machine_code.append(self.current_address & 0xFF)
#         machine_code.append((self.current_address >> 8) & 0xFF)

#         logger.debug(f"Emitting END at address {self.current_address}")

#         return machine_code






# ----------------------------------------------------------------------------------
# OLD CODE (deprecated): only BRK

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
