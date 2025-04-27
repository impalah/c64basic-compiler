def generate_code(ast):
    code = bytearray()

    # -----------------------------------------------
    # 1. Generate BASIC header that makes SYS jump to our code
    # -----------------------------------------------
    basic_start_addr = 0x0801

    # Temporal BASIC line
    basic_line = bytearray()

    sys_line_number = 10
    sys_token = 0x9E  # SYS token in BASIC V2

    # Placeholder for the next line address
    basic_line += (0x0000).to_bytes(2, "little")  # Temporal address
    basic_line += (sys_line_number).to_bytes(2, "little")
    basic_line.append(sys_token)
    basic_line.append(0x20)  # space

    # By now use "XXXX" as a placeholder for the SYS address
    # This will be corrected later
    fake_sys_addr_str = "0000"
    for c in fake_sys_addr_str:
        basic_line.append(ord(c))

    basic_line.append(0x00)  # End of line
    basic_line += (0x0000).to_bytes(2, "little")  # End of basic program

    # Now we know that the BASIC code starts after the header
    start_machine_code_addr = basic_start_addr + len(basic_line)

    # Correct the SYS address in the BASIC line
    basic_line[6] = ord(str(start_machine_code_addr)[0])
    basic_line[7] = ord(str(start_machine_code_addr)[1])
    basic_line[8] = ord(str(start_machine_code_addr)[2])
    basic_line[9] = ord(str(start_machine_code_addr)[3])

    # Correct next line pointer
    next_line_addr = (
        basic_start_addr + len(basic_line) - 4
    )  # Last 2 bytes are the end of BASIC program
    basic_line[0] = next_line_addr & 0xFF
    basic_line[1] = (next_line_addr >> 8) & 0xFF

    # Add the corrected BASIC header to the code
    code += basic_line

    # -----------------------------------------------
    # 2. Firts pass: calculate addresses for each instruction
    # -----------------------------------------------
    machine_code = bytearray()
    current_addr = start_machine_code_addr
    line_addresses = {}

    for instr in ast:
        line_addresses[instr["line"]] = current_addr

        if instr["command"] == "PRINT":
            text = " ".join(instr["args"]).strip('"')
            current_addr += (
                len(text) * 5 + 5
            )  # every character takes 5 bytes (LDA, char, JSR, LDA, char) + 5 for the final CR

        elif instr["command"] == "GOTO":
            current_addr += 3  # JMP absolute (3 bytes)

        elif instr["command"] == "END":
            current_addr += 1  # BRK (1 byte)

    # -----------------------------------------------
    # 3. Next step: generate machine code
    # -----------------------------------------------
    for instr in ast:
        if instr["command"] == "PRINT":
            text = " ".join(instr["args"]).strip('"')
            for c in text:
                machine_code.append(0xA9)  # LDA #
                machine_code.append(ord(c))
                machine_code.append(0x20)  # JSR
                machine_code.append(0xD2)
                machine_code.append(0xFF)
            machine_code.append(0xA9)
            machine_code.append(13)
            machine_code.append(0x20)
            machine_code.append(0xD2)
            machine_code.append(0xFF)

        elif instr["command"] == "GOTO":
            target_line = int(instr["args"][0])
            target_addr = line_addresses.get(target_line)
            if target_addr is None:
                raise Exception(f"Destination line {target_line} not found.")

            machine_code.append(0x4C)  # JMP absoluto
            machine_code.append(target_addr & 0xFF)
            machine_code.append((target_addr >> 8) & 0xFF)

        elif instr["command"] == "END":
            machine_code.append(0x00)  # BRK

    # -----------------------------------------------
    # 4. Combine BASIC header and machine code
    # -----------------------------------------------
    code += machine_code

    return code
