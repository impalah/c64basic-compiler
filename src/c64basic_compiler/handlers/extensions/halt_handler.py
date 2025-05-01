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
from c64basic_compiler.utils.logging import logger


class HaltHandler(InstructionHandler):
    """Handler for the HALT instruction in BASIC.
    Stops the program and waits for a key press.
    This is a custom extension to the BASIC compiler.
    It is not part of the original BASIC language.
    It is used to provide a way to stop the program and return to the BASIC prompt.

    Args:
        InstructionHandler (_type_): _description_
    """

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

        logger.debug(f"HALT handler: {len(machine_code)} bytes")

        return machine_code
