from c64basic_compiler.basic.basic_function import BasicFunction, Type


class StrFunction(BasicFunction):
    """
    Implements the BASIC 'STR$' function.

    Converts a numeric value to its string representation.

    Args:
        x: Numeric value to convert

    Returns:
        String representation of the numeric value

    Examples:
        STR$(5) = "5"
        STR$(3.14) = "3.14"
        STR$(-10) = "-10"
    """

    name = "STR$"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.STR


class ChrFunction(BasicFunction):
    """
    Implements the BASIC 'CHR$' function.

    Returns a one-character string corresponding to the specified ASCII/PETSCII code.

    Args:
        x: Integer value representing an ASCII/PETSCII code (0-255)

    Returns:
        A single character string corresponding to the code

    Examples:
        CHR$(65) = "A"
        CHR$(13) = [carriage return character]
        CHR$(32) = " " [space character]
    """

    name = "CHR$"
    arity = 1
    arg_types = [Type.INT]
    return_type = Type.STR


class AscFunction(BasicFunction):
    """
    Implements the BASIC 'ASC' function.

    Returns the ASCII/PETSCII code for the first character of a string.

    Args:
        s: String value (must not be empty)

    Returns:
        Integer ASCII/PETSCII code of the first character

    Examples:
        ASC("A") = 65
        ASC("HELLO") = 72 (ASCII/PETSCII code for 'H')
    """

    name = "ASC"
    arity = 1
    arg_types = [Type.STR]
    return_type = Type.INT


class ValFunction(BasicFunction):
    """
    Implements the BASIC 'VAL' function.

    Converts a string representation of a number to its numeric value.
    If the string doesn't start with a valid number, returns 0.

    Args:
        s: String to convert

    Returns:
        Numeric value parsed from the string

    Examples:
        VAL("123") = 123
        VAL("3.14") = 3.14
        VAL("-10") = -10
        VAL("X123") = 0 (doesn't start with a valid number)
    """

    name = "VAL"
    arity = 1
    arg_types = [Type.STR]
    return_type = Type.NUM


class LenFunction(BasicFunction):
    """
    Implements the BASIC 'LEN' function.

    Returns the length (number of characters) of a string.

    Args:
        s: String to measure

    Returns:
        Integer length of the string

    Examples:
        LEN("") = 0
        LEN("HELLO") = 5
        LEN("A B C") = 5
    """

    name = "LEN"
    arity = 1
    arg_types = [Type.STR]
    return_type = Type.INT
