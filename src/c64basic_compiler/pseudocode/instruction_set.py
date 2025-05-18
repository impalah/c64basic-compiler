from .instruction import Instruction

INSTRUCTION_SET = {
    "PUSH_CONST": Instruction(
        "PUSH_CONST", 0x01, 1
    ),  # Empuja constante (número o cadena literal)
    "PUSH_VAR": Instruction("PUSH_VAR", 0x02, 1),  # Empuja valor de variable
    "STORE_VAR": Instruction("STORE_VAR", 0x03, 1),  # Guarda valor de pila en variable
    "ADD": Instruction("ADD", 0x04, 0),  # Suma top 2 valores de pila
    "SUB": Instruction("SUB", 0x05, 0),  # Resta top 2 valores de pila
    "MUL": Instruction("MUL", 0x06, 0),  # Multiplica top 2 valores de pila
    "DIV": Instruction("DIV", 0x07, 0),  # Divide top 2 valores de pila
    "NEG": Instruction("NEG", 0x08, 0),  # Niega (cambia signo del top de la pila)
    "ABS": Instruction("ABS", 0x09, 0),  # Valor absoluto del top de la pila
    "PEEK": Instruction("PEEK", 0x0A, 0),  # Lee memoria en dirección del top de la pila
    "POKE": Instruction(
        "POKE", 0x0B, 0
    ),  # Escribe valor en dirección (top 2 de pila: dirección, valor)
    "LEN": Instruction("LEN", 0x0C, 0),  # Longitud de cadena (top de la pila)
    "CHR$": Instruction(
        "CHR$", 0x0D, 0
    ),  # Devuelve carácter como string desde código ASCII
    "PRINT": Instruction("PRINT", 0x0E, 0),  # Imprime valor de pila
    "JMP": Instruction("JMP", 0x0F, 1),  # Salto incondicional a dirección
    "JZ": Instruction("JZ", 0x10, 1),  # Salta si top de la pila es cero
    "JNZ": Instruction("JNZ", 0x11, 1),  # Salta si top de la pila es no-cero
    "CALL": Instruction("CALL", 0x12, 1),  # Llama a subrutina por nombre o ID
    "RET": Instruction("RET", 0x13, 0),  # Retorna de subrutina
    "NOP": Instruction("NOP", 0x14, 0),  # No hace nada (para alineación o debugging)
    "LABEL": Instruction(
        "LABEL", 0x15, 1
    ),  # Marca una posición en el flujo para saltos
    "EQ": Instruction("EQ", 0x16, 0),  # Compara top 2; push 1 si iguales, 0 si no
    "NEQ": Instruction("NEQ", 0x17, 0),  # Push 1 si distintos, 0 si no
    "GT": Instruction("GT", 0x18, 0),  # Push 1 si a > b
    "LT": Instruction("LT", 0x19, 0),  # Push 1 si a < b
    "GTE": Instruction("GTE", 0x1A, 0),  # Push 1 si a ≥ b
    "LTE": Instruction("LTE", 0x1B, 0),  # Push 1 si a ≤ b
    "AND": Instruction("AND", 0x1C, 0),  # Lógico: top 2 de pila
    "OR": Instruction("OR", 0x1D, 0),  # Lógico: top 2 de pila
    "NOT": Instruction(
        "NOT", 0x1E, 0
    ),  # Lógico: invierte top de la pila (0→1, no cero→0)
    "STR_EQ": Instruction("STR_EQ", 0x1F, 0),  # Compara 2 strings por igualdad
    "CONCAT": Instruction("CONCAT", 0x20, 0),  # Concatena top 2 cadenas
    "MID$": Instruction("MID$", 0x21, 0),  # MID$(s$, start, len): requiere 3 valores
    "LEFT$": Instruction("LEFT$", 0x22, 0),  # LEFT$(s$, n)
    "RIGHT$": Instruction("RIGHT$", 0x23, 0),  # RIGHT$(s$, n)
    "VAL": Instruction("VAL", 0x24, 0),  # Convierte cadena a número
    "STR$": Instruction("STR$", 0x25, 0),  # Convierte número a cadena
    "INPUT": Instruction(
        "INPUT", 0x26, 1
    ),  # Lee entrada del usuario y la guarda en variable
    "END": Instruction("END", 0x27, 0),  # Termina el programa
    "REM": Instruction("REM", 0x28, 1),  # Comentario (ignorado en tiempo de ejecución)
}
