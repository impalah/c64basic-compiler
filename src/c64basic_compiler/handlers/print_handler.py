# c64basic_compiler/handlers/print_handler.py

from c64basic_compiler.handlers.instruction_handler import (
    InstructionHandler,
)
import c64basic_compiler.common.opcodes_6502 as opcodes
import c64basic_compiler.common.kernal_routines as kernal
from c64basic_compiler.common.petscii_map import PETSCII_CONTROL
from c64basic_compiler.utils.print_utils import parse_print_args
from c64basic_compiler.utils.logging import logger


BASE_VARIABLES_ADDR = 0xC000


class PrintHandler(InstructionHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_machine_code = None  # Cache para el código máquina

    def size(self) -> int:
        """
        Calculate the size of the PRINT instruction by using the cached machine code.
        """
        if self._cached_machine_code is None:
            self._cached_machine_code = self.emit()  # Generar y cachear el código máquina
        size = len(self._cached_machine_code)  # Calcular el tamaño real
        logger.debug(f"Real size for PRINT instruction: {size} bytes")
        return size

    def emit(self) -> bytearray:
        """
        Generate the machine code for the PRINT instruction, using the cache if available.
        """
        if self._cached_machine_code is not None:
            logger.debug("Using cached machine code for PRINT instruction")
            return self._cached_machine_code

        machine_code = bytearray()

        logger.debug(f"PRINT instruction. Arguments {self.instr['args']}")

        symbol_table = self.context.symbol_table
        args = parse_print_args(self.instr["args"])

        for arg in args:
            if arg["type"] == "string":
                for c in arg["value"]:
                    machine_code.append(opcodes.LDA_IMMEDIATE)
                    machine_code.append(ord(c))
                    machine_code.append(opcodes.JSR_ABSOLUTE)
                    machine_code.append(kernal.CHROUT & 0xFF)
                    machine_code.append((kernal.CHROUT >> 8) & 0xFF)

            elif arg["type"] == "variable":
                varname = arg["value"]

                if varname not in symbol_table:
                    raise Exception(f"Variable '{varname}' no encontrada para PRINT.")

                var_type = symbol_table.get_type(varname)
                address = symbol_table.get_address(varname)

                if var_type == "string":
                    # Leer puntero a cadena desde variable (2 bytes)
                    # Cargar lo
                    machine_code.append(opcodes.LDA_ABSOLUTE)
                    machine_code.append(address & 0xFF)
                    machine_code.append((address >> 8) & 0xFF)
                    machine_code.append(opcodes.STA_ABSOLUTE)
                    machine_code.append(0xFB)
                    machine_code.append(0x00)

                    # Cargar hi
                    machine_code.append(opcodes.LDA_ABSOLUTE)
                    machine_code.append((address + 1) & 0xFF)
                    machine_code.append(((address + 1) >> 8) & 0xFF)
                    machine_code.append(opcodes.STA_ABSOLUTE)
                    machine_code.append(0xFC)
                    machine_code.append(0x00)

                    # LDY #$00
                    machine_code.append(opcodes.LDY_IMMEDIATE)
                    machine_code.append(0x00)

                    # Bucle de impresión
                    loop_start = len(machine_code)

                    # LDA ($FB),Y
                    machine_code.append(opcodes.LDA_INDIRECT_INDEXED)
                    machine_code.append(0xFB)

                    # CMP #0
                    machine_code.append(opcodes.CMP_IMMEDIATE)
                    machine_code.append(0x00)

                    # BEQ salir
                    machine_code.append(opcodes.BEQ)
                    machine_code.append(0x06)  # salto a final

                    # JSR_ABSOLUTE CHROUT
                    machine_code.append(opcodes.JSR_ABSOLUTE)
                    machine_code.append(kernal.CHROUT & 0xFF)
                    machine_code.append((kernal.CHROUT >> 8) & 0xFF)

                    # INY
                    machine_code.append(opcodes.INY)

                    # JMP loop
                    machine_code.append(opcodes.JMP_ABSOLUTE)
                    jump_target = loop_start
                    machine_code.append(jump_target & 0xFF)
                    machine_code.append((jump_target >> 8) & 0xFF)

                    # salida

                else:  # tipo number
                    machine_code.append(opcodes.LDA_ABSOLUTE)
                    machine_code.append(address & 0xFF)
                    machine_code.append((address >> 8) & 0xFF)
                    machine_code.append(opcodes.ADC_IMMEDIATE)
                    machine_code.append(0x30)
                    machine_code.append(opcodes.JSR_ABSOLUTE)
                    machine_code.append(kernal.CHROUT & 0xFF)
                    machine_code.append((kernal.CHROUT >> 8) & 0xFF)

        # CR final
        machine_code.append(opcodes.LDA_IMMEDIATE)
        machine_code.append(PETSCII_CONTROL["CR"])
        machine_code.append(opcodes.JSR_ABSOLUTE)
        machine_code.append(kernal.CHROUT & 0xFF)
        machine_code.append((kernal.CHROUT >> 8) & 0xFF)

        logger.debug(f"Emitting PRINT at address {self.current_address}")
        logger.debug(f"PRINT Machine code: {machine_code.hex()}")

        self._cached_machine_code = machine_code  # Cachear el código máquina generado
        return machine_code