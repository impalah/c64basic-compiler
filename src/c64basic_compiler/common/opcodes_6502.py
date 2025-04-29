# c64basic_compiler/common/opcodes_6502.py

# -------------------------------
# 6502 Opcodes - Assembler mnemonics
# -------------------------------

# Memory & Accumulator Operations
LDA_INDIRECT_INDEXED = 0xB1  # LDA ($addr),Y
STA_INDIRECT_INDEXED = 0x91  # STA ($addr),Y
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
JSR_ABSOLUTE = 0x20  # Jump to SubRoutine
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

INY = 0xC8  # Increment Y
DEY = 0x88  # Decrement Y
INX = 0xE8  # Increment X
DEX = 0xCA  # Decrement X
TAY = 0xA8  # Transfer Accumulator to Y
TAX = 0xAA  # Transfer Accumulator to X
TYA = 0x98  # Transfer Y to Accumulator
TXA = 0x8A  # Transfer X to Accumulator
TSX = 0xBA  # Transfer Stack Pointer to X
TXS = 0x9A  # Transfer X to Stack Pointer
STY_ABSOLUTE = 0x8C  # Store Y Register to absolute address
STX_ABSOLUTE = 0x8E  # Store X Register to absolute address
STY_ZERO_PAGE = 0x84  # Store Y Register to zero page
STX_ZERO_PAGE = 0x86  # Store X Register to zero page
LDY_ABSOLUTE = 0xAC  # Load Y Register from absolute address
LDX_ABSOLUTE = 0xAE  # Load X Register from absolute address
LDY_ZERO_PAGE = 0xA4  # Load Y Register from zero page
LDX_ZERO_PAGE = 0xA6  # Load X Register from zero page
# Zero Page Operations
LDA_ZERO_PAGE = 0xA5  # Load Accumulator from zero page
STA_ZERO_PAGE = 0x85  # Store Accumulator to zero page
LDA_ZERO_PAGE_X = 0xB5  # Load Accumulator from zero page, X offset
STA_ZERO_PAGE_X = 0x95  # Store Accumulator to zero page, X offset
LDA_ZERO_PAGE_Y = 0xB6  # Load Accumulator from zero page, Y offset
STA_ZERO_PAGE_Y = 0x96  # Store Accumulator to zero page, Y offset
LDA_ABSOLUTE_X = 0xBD  # Load Accumulator from absolute address, X offset
STA_ABSOLUTE_X = 0x9D  # Store Accumulator to absolute address, X offset
LDA_ABSOLUTE_Y = 0xB9  # Load Accumulator from absolute address, Y offset
STA_ABSOLUTE_Y = 0x99  # Store Accumulator to absolute address, Y offset
LDA_INDIRECT_X = 0xA1  # Load Accumulator from indirect address, X offset
STA_INDIRECT_X = 0x81  # Store Accumulator to indirect address, X offset
