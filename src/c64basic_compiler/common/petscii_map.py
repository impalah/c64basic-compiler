# c64basic_compiler/common/petscii_map.py

# ---------------------------------------------------
# PETSCII Character Map - Commodore 64
# ---------------------------------------------------
# PETSCII (PET Standard Code of Information Interchange)
# ---------------------------------------------------
# PETSCII is the character set used by Commodore computers,
# including the Commodore 64. It is a variant of ASCII
# (American Standard Code for Information Interchange) with
# additional graphics and control characters. PETSCII is
# used for text display, graphics, and control of the
# Commodore 64's screen and keyboard.
# Printable PETSCII Characters (Screen codes)
# Based on C64 default mode (unshifted, shifted)

# -----------------------------------
# Números
# -----------------------------------
PETSCII_NUMBERS = {
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
}

# -----------------------------------
# Letras mayúsculas (A-Z)
# -----------------------------------
PETSCII_UPPERCASE = {chr(65 + i): 0x41 + i for i in range(26)}

# -----------------------------------
# Letras minúsculas (a-z) (depende del modo C64)
# Cuidado: en modo C64 "normal" las letras pequeñas son gráficos.
# Se incluye aquí para traducciones personalizadas.
# PETSCII modo shifted/minúsculas
PETSCII_LOWERCASE = {chr(97 + i): 0x61 + i for i in range(26)}

# -----------------------------------
# Caracteres especiales y signos de puntuación
# -----------------------------------
PETSCII_SYMBOLS = {
    " ": 0x20,
    "!": 0x21,
    '"': 0x22,
    "#": 0x23,
    "$": 0x24,
    "%": 0x25,
    "&": 0x26,
    "'": 0x27,
    "(": 0x28,
    ")": 0x29,
    "*": 0x2A,
    "+": 0x2B,
    ",": 0x2C,
    "-": 0x2D,
    ".": 0x2E,
    "/": 0x2F,
    ":": 0x3A,
    ";": 0x3B,
    "<": 0x3C,
    "=": 0x3D,
    ">": 0x3E,
    "?": 0x3F,
    "@": 0x40,
    "[": 0x5B,
    "\\": 0x5C,
    "]": 0x5D,
    "^": 0x5E,
    "_": 0x5F,
}

# -----------------------------------
# Caracteres gráficos básicos
# (bloques, líneas, cuadros, etc.)
# -----------------------------------
PETSCII_GRAPHICS = {
    "█": 0xDB,  # Bloque completo
    "▄": 0xDC,  # Bloque inferior
    "▌": 0xDD,  # Bloque izquierdo
    "▐": 0xDE,  # Bloque derecho
    "▀": 0xDF,  # Bloque superior
}

# -----------------------------------
# Control Characters (Movimientos del cursor, etc.)
# -----------------------------------
PETSCII_CONTROL = {
    "CR": 0x0D,  # Carriage Return
    "HOME": 0x13,  # Mover cursor a Home
    "CLR": 0x93,  # Clear Screen
    "INST/DEL": 0x14,
    "CURSOR_UP": 0x91,
    "CURSOR_DOWN": 0x11,
    "CURSOR_LEFT": 0x9D,
    "CURSOR_RIGHT": 0x1D,
}

# -----------------------------------
# Unión de todo para búsquedas rápidas
# -----------------------------------
PETSCII_ALL = {}
PETSCII_ALL.update(PETSCII_NUMBERS)
PETSCII_ALL.update(PETSCII_UPPERCASE)
PETSCII_ALL.update(PETSCII_LOWERCASE)
PETSCII_ALL.update(PETSCII_SYMBOLS)
PETSCII_ALL.update(PETSCII_GRAPHICS)
PETSCII_ALL.update(PETSCII_CONTROL)

# Puedes buscar fácilmente:
# PETSCII_ALL.get('A') -> 0x41
# PETSCII_ALL.get(' ') -> 0x20
