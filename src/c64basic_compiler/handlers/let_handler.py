# c64basic_compiler/handlers/let_handler.py

import c64basic_compiler.common.opcodes_6502 as opcodes
from c64basic_compiler.handlers.instruction_handler import InstructionHandler


BASE_VARIABLES_ADDR = 0xC000


class LetHandler(InstructionHandler):
    def normalize_varname(self, name: str) -> str:
        name = name.upper()
        if not name[0].isalpha():
            raise ValueError(
                f"Invalid variable name (must start with a letter): {name}"
            )
        if len(name) > 255:
            raise ValueError(f"Variable name too long: {name}")
        if not all(c.isalnum() or c == "$" for c in name):
            raise ValueError(
                f"Variable name can only contain letters, numbers and $: {name}"
            )
        return name  # no cortamos a 2 chars, ya que estás permitiendo 255

    def size(self) -> int:
        # LDA + dato o LDA + dirección + STA + dirección → estimado máximo
        return 10

    def emit(self) -> bytearray:
        machine_code = bytearray()

        varname = self.normalize_varname(self.instr["args"][0])
        symbol_table = self.context.symbol_table

        var_type = "string" if varname.endswith("$") else "number"
        target_address = symbol_table.register(varname, var_type)

        value_token = self.instr["args"][2]

        # --- CASO 1: asignación de cadena literal ---
        if value_token.startswith('"') and value_token.endswith('"'):
            if var_type != "string":
                raise Exception(
                    f"Cannot assign a string to non-string variable '{varname}'."
                )

            string_literal = value_token.strip('"')
            string_area = self.context.string_area
            str_address = string_area.store_string(string_literal)

            # LDA #low(str_address)
            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append(str_address & 0xFF)
            # STA target_address
            machine_code.append(opcodes.STA_ABSOLUTE)
            machine_code.append(target_address & 0xFF)
            machine_code.append((target_address >> 8) & 0xFF)

            # LDA #high(str_address)
            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append((str_address >> 8) & 0xFF)
            # STA target_address + 1
            machine_code.append(opcodes.STA_ABSOLUTE)
            machine_code.append((target_address + 1) & 0xFF)
            machine_code.append(((target_address + 1) >> 8) & 0xFF)

            return machine_code

        # --- CASO 2: asignación de número inmediato ---
        if value_token.isdigit():
            if var_type != "number":
                raise Exception(f"Cannot assign number to string variable '{varname}'.")

            value = int(value_token)
            machine_code.append(opcodes.LDA_IMMEDIATE)
            machine_code.append(value)

        # --- CASO 3: asignación de variable a variable ---
        else:
            src_varname = self.normalize_varname(value_token)

            if src_varname not in symbol_table:
                raise Exception(f"Source variable '{src_varname}' not defined.")

            src_address = symbol_table.get_address(src_varname)

            if var_type == "string":
                # Copiar 2 bytes de dirección (puntero a cadena)
                # LDA src lo
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append(src_address & 0xFF)
                machine_code.append((src_address >> 8) & 0xFF)
                # STA target lo
                machine_code.append(opcodes.STA_ABSOLUTE)
                machine_code.append(target_address & 0xFF)
                machine_code.append((target_address >> 8) & 0xFF)

                # LDA src hi
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append((src_address + 1) & 0xFF)
                machine_code.append(((src_address + 1) >> 8) & 0xFF)
                # STA target hi
                machine_code.append(opcodes.STA_ABSOLUTE)
                machine_code.append((target_address + 1) & 0xFF)
                machine_code.append(((target_address + 1) >> 8) & 0xFF)

                return machine_code
            else:
                # variable numérica
                machine_code.append(opcodes.LDA_ABSOLUTE)
                machine_code.append(src_address & 0xFF)
                machine_code.append((src_address >> 8) & 0xFF)

        # STA target_address (para variable numérica)
        machine_code.append(opcodes.STA_ABSOLUTE)
        machine_code.append(target_address & 0xFF)
        machine_code.append((target_address >> 8) & 0xFF)

        return machine_code
