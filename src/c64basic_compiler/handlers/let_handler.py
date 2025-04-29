# c64basic_compiler/handlers/let_handler.py

import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.handlers.instruction_handler import InstructionHandler

class LetHandler(InstructionHandler):
    def normalize_varname(self, name: str) -> str:
        name = name.upper()
        if not name[0].isalpha():
            raise ValueError(f"Invalid variable name (must start with a letter): {name}")
        if len(name) > 255:
            raise ValueError(f"Variable name too long: {name}")
        if not all(c.isalnum() or c == "$" for c in name):
            raise ValueError(f"Variable name can only contain letters, numbers and $: {name}")
        return name[:2]  # C64: solo los dos primeros caracteres cuentan

    def size(self) -> int:
        # Aproximadamente 5 bytes: LDA + dato o dirección + STA dirección
        return 5

    def emit(self) -> bytearray:
        machine_code = bytearray()

        # Args ejemplo: ['A', '=', '5'] o ['A', '=', 'B']
        varname = self.normalize_varname(self.instr["args"][0])
        symbol_table = self.context.symbol_table

        var_type = "string" if varname.endswith("$") else "number"
        target_address = symbol_table.register(varname, var_type)

        value_token = self.instr["args"][2]

        if value_token.isdigit():
            # Asignación inmediata de número
            value = int(value_token)

            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append(value)

        else:
            # Asignación de una variable a otra
            src_varname = self.normalize_varname(value_token)

            if src_varname not in symbol_table:
                raise Exception(f"Source variable '{src_varname}' not defined.")

            src_address = symbol_table.get_address(src_varname)

            machine_code.append(opcodes.LDA_ABSOLUTE)
            machine_code.append(src_address & 0xFF)
            machine_code.append((src_address >> 8) & 0xFF)

        # STA target_address
        machine_code.append(opcodes.STA_ABSOLUTE)
        machine_code.append(target_address & 0xFF)
        machine_code.append((target_address >> 8) & 0xFF)

        return machine_code
