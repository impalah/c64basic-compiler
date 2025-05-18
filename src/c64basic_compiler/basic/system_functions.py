from c64basic_compiler.basic.basic_function import BasicFunction, Type


class PeekFunction(BasicFunction):
    """
    Implements the BASIC 'PEEK' function.

    Reads a byte value (0-255) from a specific memory address.

    Args:
        addr: Integer memory address (0-65535)

    Returns:
        Byte value (0-255) at the specified memory address

    Examples:
        PEEK(53280) = 14  (might return the current border color)
        PEEK(1024) = 1    (first character in screen memory)
    """

    name = "PEEK"
    arity = 1
    arg_types = [Type.INT]
    return_type = Type.INT


class TiFunction(BasicFunction):
    """
    Implements the BASIC 'TI' function.

    Returns the number of 1/60ths of a second elapsed since the computer was turned on
    or since this value was last set. (Often known as "jiffies")

    Args:
        None

    Returns:
        Integer representing elapsed jiffies

    Examples:
        TI = 36000  (after 10 minutes)
    """

    name = "TI"
    arity = 0
    arg_types = []
    return_type = Type.INT


class TiStringFunction(BasicFunction):
    """
    Implements the BASIC 'TI$' function.

    Returns the current time as a 6-digit string in "HHMMSS" format
    (hours, minutes, seconds).

    Args:
        None

    Returns:
        String representing current time in "HHMMSS" format

    Examples:
        TI$ = "104523"  (10:45:23)
    """

    name = "TI$"
    arity = 0
    arg_types = []
    return_type = Type.STR


class TimeFunction(BasicFunction):
    """
    Implements the BASIC 'TIME' function.

    Alternative name for TI in some BASIC dialects. Returns the number of
    1/60ths of a second elapsed since the computer was turned on or reset.

    Args:
        None

    Returns:
        Integer representing elapsed jiffies

    Examples:
        TIME = 18000  (after 5 minutes)
    """

    name = "TIME"
    arity = 0
    arg_types = []
    return_type = Type.INT


class TimeStringFunction(BasicFunction):
    """
    Implements the BASIC 'TIME$' function.

    Alternative name for TI$ in some BASIC dialects. Returns the current time
    as a 6-digit string in "HHMMSS" format (hours, minutes, seconds).

    Args:
        None

    Returns:
        String representing current time in "HHMMSS" format

    Examples:
        TIME$ = "153045"  (15:30:45)
    """

    name = "TIME$"
    arity = 0
    arg_types = []
    return_type = Type.STR


class PiFunction(BasicFunction):
    """
    Implements the BASIC 'PI' function.

    Returns the mathematical constant π (pi).

    Args:
        None

    Returns:
        The value of π (approximately 3.14159...)

    Examples:
        PI = 3.14159...
        2*PI = 6.28318... (circumference of a unit circle)
    """

    name = "PI"
    arity = 0
    arg_types = []
    return_type = Type.NUM
