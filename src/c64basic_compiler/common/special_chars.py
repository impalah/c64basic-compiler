# c64basic_compiler/common/special_chars.py

# ---------------------------------------------------
# Special Character Codes for Commodore 64 (PETSCII)
# ---------------------------------------------------
# PETSCII is not the same as ASCII exactly, but for
# simple control characters they are compatible.

# Control Characters
CHAR_NULL = 0x00  # NUL - End of BASIC line
CHAR_BEL = 0x07  # BEL - Bell
CHAR_BS = 0x08  # BS  - Backspace
CHAR_TAB = 0x09  # HT  - Horizontal Tab
CHAR_LF = 0x0A  # LF  - Line Feed (rarely used)
CHAR_CR = 0x0D  # CR  - Carriage Return (RETURN key)
CHAR_ESC = 0x1B  # ESC - Escape
CHAR_SPACE = 0x20  # SPACE

# Printable ASCII/PETSCII range starts at 0x20 (SPACE)

# Additional Commodore 64 Special Keys
CHAR_RUNSTOP = 0x03  # RUN/STOP Key (in raw key matrix)
CHAR_SHIFT = 0x01  # SHIFT (modifier, not printable)

# PETSCII-specific codes
CHAR_CURSOR_UP = 0x91
CHAR_CURSOR_DOWN = 0x11
CHAR_CURSOR_LEFT = 0x9D
CHAR_CURSOR_RIGHT = 0x1D

CHAR_CLEAR_SCREEN = 0x93  # Clear screen character in PETSCII

# Optional: Standard ASCII printable characters
CHAR_QUOTE = 0x22  # "
CHAR_COMMA = 0x2C  # ,
CHAR_SEMICOLON = 0x3B  # ;
CHAR_DOLLAR = 0x24  # $
