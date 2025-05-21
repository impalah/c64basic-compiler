from dataclasses import dataclass


@dataclass
class Instruction:
    """Definición de una instrucción de pseudocódigo."""

    mnemonic: str  # Nombre textual (ej. "PUSH_CONST")
    opcode: int  # Código binario (ej. 0x01)
    operand_count: int  # Cuántos operandos espera
