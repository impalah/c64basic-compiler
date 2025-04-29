# c64basic_compiler/handlers/print_handler.py

from c64basic_compiler.handlers.instruction_handler import InstructionHandler
import c64basic_compiler.common.opcodes_6502 as opcodes
import c64basic_compiler.common.kernal_routines as kernal
from c64basic_compiler.common.petscii_map import PETSCII_ALL, PETSCII_CONTROL

class PrintHandler(InstructionHandler):
    def size(self) -> int:
        return 80  # Estimación general para múltiples argumentos

    def emit(self) -> bytearray:
        machine_code = bytearray()
        symbol_table = self.context.symbol_table

        args = self.instr["args"]
        i = 0
        while i < len(args):
            token = args[i]

            if token == ",":
                # Tabulación a siguiente zona (simplificado: insertar un espacio)
                machine_code.append(opcodes.LDA_IMMEDIATE)
                machine_code.append(PETSCII_ALL.get(" ", 0x20))
                machine_code.append(opcodes.JSR)
                machine_code.append(kernal.CHROUT & 0xFF)
                machine_code.append((kernal.CHROUT >> 8) & 0xFF)
                i += 1
                continue

            elif token == ";":
                # Punto y coma = no hacer nada especial (impresión continua)
                i += 1
                continue

            elif token.startswith('"') and token.endswith('"'):
                text = token.strip('"')
                for c in text:
                    petscii = PETSCII_ALL.get(c.upper(), ord(c))
                    machine_code.append(opcodes.LDA_IMMEDIATE)
                    machine_code.append(petscii)
                    machine_code.append(opcodes.JSR)
                    machine_code.append(kernal.CHROUT & 0xFF)
                    machine_code.append((kernal.CHROUT >> 8) & 0xFF)
                i += 1

            else:
                varname = token.upper()[:2]
                if varname not in symbol_table:
                    raise Exception(f"Variable {varname} no encontrada para PRINT.")
                address = symbol_table.get_address(varname)
                var_type = symbol_table.get_type(varname)

                if var_type == "number":
                    machine_code.append(opcodes.LDA_ABSOLUTE)
                    machine_code.append(address & 0xFF)
                    machine_code.append((address >> 8) & 0xFF)
                    machine_code.append(opcodes.ADC_IMMEDIATE)
                    machine_code.append(0x30)
                    machine_code.append(opcodes.JSR)
                    machine_code.append(kernal.CHROUT & 0xFF)
                    machine_code.append((kernal.CHROUT >> 8) & 0xFF)

                elif var_type == "string":
                    machine_code.append(opcodes.LDA_ABSOLUTE)
                    machine_code.append(address & 0xFF)
                    machine_code.append((address >> 8) & 0xFF)
                    machine_code.append(opcodes.STA_ABSOLUTE)
                    machine_code.append(0xFB)
                    machine_code.append(0x00)

                    machine_code.append(opcodes.LDA_ABSOLUTE)
                    machine_code.append((address + 1) & 0xFF)
                    machine_code.append(((address + 1) >> 8) & 0xFF)
                    machine_code.append(opcodes.STA_ABSOLUTE)
                    machine_code.append(0xFC)
                    machine_code.append(0x00)

                    machine_code.append(opcodes.LDY_IMMEDIATE)
                    machine_code.append(0x00)

                    loop_start = len(machine_code)

                    machine_code.append(opcodes.LDA_INDIRECT_INDEXED)
                    machine_code.append(0xFB)

                    machine_code.append(opcodes.CMP_IMMEDIATE)
                    machine_code.append(0x00)

                    machine_code.append(opcodes.BEQ)
                    machine_code.append(0x0A)  # salto al final del bucle

                    machine_code.append(opcodes.JSR)
                    machine_code.append(kernal.CHROUT & 0xFF)
                    machine_code.append((kernal.CHROUT >> 8) & 0xFF)

                    machine_code.append(opcodes.INY)

                    machine_code.append(opcodes.JMP_ABSOLUTE)
                    jmp_back_addr = len(machine_code)
                    machine_code += [0x00, 0x00]  # placeholder

                    loop_addr = loop_start
                    machine_code[jmp_back_addr] = loop_addr & 0xFF
                    machine_code[jmp_back_addr + 1] = (loop_addr >> 8) & 0xFF

                else:
                    raise Exception(f"Tipo de variable {varname} no soportado en PRINT.")

                i += 1

        # Añadir RETURN (CR) al final
        machine_code.append(opcodes.LDA_IMMEDIATE)
        machine_code.append(PETSCII_CONTROL["CR"])
        machine_code.append(opcodes.JSR)
        machine_code.append(kernal.CHROUT & 0xFF)
        machine_code.append((kernal.CHROUT >> 8) & 0xFF)

        return machine_code
