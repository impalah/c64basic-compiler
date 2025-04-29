# c64basic_compiler/common/basic_tokens.py

# ---------------------------------------------------
# C64 BASIC V2 Tokens
# ---------------------------------------------------
# Every token is defined by its hexadecimal value.
# ---------------------------------------------------

# BASIC Commands
END = 0x80
FOR = 0x81
NEXT = 0x82
DATA = 0x83
INPUT_HASH = 0x84  # INPUT#
INPUT = 0x85
DIM = 0x86
READ = 0x87
LET = 0x88
GOTO = 0x89
RUN = 0x8A
IF = 0x8B
RESTORE = 0x8C
GOSUB = 0x8D
RETURN = 0x8E
REM = 0x8F
STOP = 0x90
ON = 0x91
WAIT = 0x92
LOAD = 0x93
SAVE = 0x94
VERIFY = 0x95
DEF = 0x96
POKE = 0x97
PRINT_HASH = 0x98  # PRINT#
PRINT = 0x99
CONT = 0x9A
LIST = 0x9B
CLR = 0x9C
CMD = 0x9D
SYS = 0x9E
OPEN = 0x9F
CLOSE = 0xA0
GET = 0xA1
NEW = 0xA2
TAB_OPEN = 0xA3  # TAB(
TO = 0xA4
FN = 0xA5
SPC_OPEN = 0xA6  # SPC(
THEN = 0xA7
NOT = 0xA8
STEP = 0xA9

# Operators
PLUS = 0xAA
MINUS = 0xAB
MULTIPLY = 0xAC
DIVIDE = 0xAD
POWER = 0xAE
AND = 0xAF
OR = 0xB0
GREATER = 0xB1
EQUAL = 0xB2
LESS = 0xB3

# Math/Function Calls
SGN = 0xB4
INT = 0xB5
ABS = 0xB6
USR = 0xB7
FRE = 0xB8
POS = 0xB9
SQR = 0xBA
RND = 0xBB
LOG = 0xBC
EXP = 0xBD
COS = 0xBE
SIN = 0xBF
TAN = 0xC0
ATN = 0xC1
PEEK = 0xC2
LEN = 0xC3
STR_DOLLAR = 0xC4
VAL = 0xC5
ASC = 0xC6
CHR_DOLLAR = 0xC7
LEFT_DOLLAR = 0xC8
RIGHT_DOLLAR = 0xC9
MID_DOLLAR = 0xCA


# ---------------------------------------------------
# List of BASIC commands (keywords) to support in the parser
# ---------------------------------------------------
SUPPORTED_COMMANDS = {
    "END", "FOR", "NEXT", "DATA", "INPUT#", "INPUT", "DIM", "READ", "LET",
    "GOTO", "RUN", "IF", "RESTORE", "GOSUB", "RETURN", "REM", "STOP", "ON",
    "WAIT", "LOAD", "SAVE", "VERIFY", "DEF", "POKE", "PRINT#", "PRINT", "CONT",
    "LIST", "CLR", "CMD", "SYS", "OPEN", "CLOSE", "GET", "NEW"
}



