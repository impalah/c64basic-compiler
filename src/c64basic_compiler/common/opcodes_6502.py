# c64basic_compiler/common/opcodes_6502.py

# -------------------------------
# 6502 Opcodes - Assembler mnemonics
# -------------------------------

# Memory & Accumulator Operations
LDA_IMMEDIATE = 0xA9  # Load Accumulator with Immediate value
LDA_ABSOLUTE = 0xAD  # Load Accumulator from absolute address
STA_ABSOLUTE = 0x8D  # Store Accumulator to absolute address
LDX_IMMEDIATE = 0xA2  # Load X Register with Immediate
LDY_IMMEDIATE = 0xA0  # Load Y Register with Immediate

# Arithmetic Operations
ADC_IMMEDIATE = 0x69  # Add with Carry Immediate
SBC_IMMEDIATE = 0xE9  # Subtract with Carry Immediate

# Logic Operations
AND_IMMEDIATE = 0x29  # Logical AND Immediate
ORA_IMMEDIATE = 0x09  # Logical OR Immediate
EOR_IMMEDIATE = 0x49  # Exclusive OR Immediate

# Comparison Operations
CMP_IMMEDIATE = 0xC9  # Compare Accumulator Immediate
CPX_IMMEDIATE = 0xE0  # Compare X Register Immediate
CPY_IMMEDIATE = 0xC0  # Compare Y Register Immediate

# Branching Operations
BEQ = 0xF0  # Branch if Equal (Zero set)
BNE = 0xD0  # Branch if Not Equal (Zero clear)
BCC = 0x90  # Branch if Carry Clear
BCS = 0xB0  # Branch if Carry Set
BMI = 0x30  # Branch if Minus (Negative set)
BPL = 0x10  # Branch if Plus (Negative clear)
BVC = 0x50  # Branch if Overflow Clear
BVS = 0x70  # Branch if Overflow Set

JMP_ABSOLUTE = 0x4C  # Jump to absolute address
JSR = 0x20  # Jump to SubRoutine
RTS = 0x60  # Return from Subroutine

# Stack Operations
PHA = 0x48  # Push Accumulator on Stack
PLA = 0x68  # Pull Accumulator from Stack
PHP = 0x08  # Push Processor Status on Stack
PLP = 0x28  # Pull Processor Status from Stack

# Status Register Operations
CLC = 0x18  # Clear Carry Flag
SEC = 0x38  # Set Carry Flag
CLD = 0xD8  # Clear Decimal Mode
SED = 0xF8  # Set Decimal Mode
CLI = 0x58  # Clear Interrupt Disable
SEI = 0x78  # Set Interrupt Disable
CLV = 0xB8  # Clear Overflow Flag

# Shifts and Rotations
ASL_ACCUMULATOR = 0x0A  # Arithmetic Shift Left (Accumulator)
LSR_ACCUMULATOR = 0x4A  # Logical Shift Right (Accumulator)
ROL_ACCUMULATOR = 0x2A  # Rotate Left (Accumulator)
ROR_ACCUMULATOR = 0x6A  # Rotate Right (Accumulator)

# Miscellaneous
NOP = 0xEA  # No Operation
BRK = 0x00  # Force Break
RTI = 0x40  # Return from Interrupt
