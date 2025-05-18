from c64basic_compiler.basic.basic_function import BasicFunction, Type


class AbsFunction(BasicFunction):
    """
    Implements the BASIC 'ABS' function.

    Returns the absolute value (magnitude) of a number.

    Args:
        x: Numeric value

    Returns:
        The absolute value of x (always non-negative)

    Examples:
        ABS(5) = 5
        ABS(-3) = 3
    """

    name = "ABS"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class IntFunction(BasicFunction):
    """
    Implements the BASIC 'INT' function.

    Returns the largest integer that is less than or equal to the argument
    (truncates toward negative infinity).

    Args:
        x: Numeric value

    Returns:
        Integer less than or equal to x

    Examples:
        INT(5.7) = 5
        INT(-3.2) = -4  (Note: not -3, as INT truncates toward negative infinity)
    """

    name = "INT"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.INT


class SgnFunction(BasicFunction):
    """
    Implements the BASIC 'SGN' function.

    Returns the sign of a number: -1 for negative, 0 for zero, 1 for positive.

    Args:
        x: Numeric value

    Returns:
        -1, 0, or 1 depending on sign of x

    Examples:
        SGN(5) = 1
        SGN(0) = 0
        SGN(-3) = -1
    """

    name = "SGN"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.INT


class SqrFunction(BasicFunction):
    """
    Implements the BASIC 'SQR' function.

    Calculates the square root of a non-negative number.

    Args:
        x: Non-negative numeric value

    Returns:
        Square root of x

    Examples:
        SQR(9) = 3
        SQR(2) = 1.4142...
    """

    name = "SQR"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class LogFunction(BasicFunction):
    """
    Implements the BASIC 'LOG' function.

    Calculates the natural logarithm (base e) of a positive number.

    Args:
        x: Positive numeric value

    Returns:
        Natural logarithm of x

    Examples:
        LOG(1) = 0
        LOG(2.718...) = 1
        LOG(10) = 2.3025...
    """

    name = "LOG"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class ExpFunction(BasicFunction):
    """
    Implements the BASIC 'EXP' function.

    Calculates e raised to the power of the argument.

    Args:
        x: Numeric value

    Returns:
        e^x (e to the power of x)

    Examples:
        EXP(0) = 1
        EXP(1) = 2.718...
        EXP(2) = 7.389...
    """

    name = "EXP"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class SinFunction(BasicFunction):
    """
    Implements the BASIC 'SIN' function.

    Calculates the sine of an angle in radians.

    Args:
        x: Angle in radians

    Returns:
        Sine of the angle

    Examples:
        SIN(0) = 0
        SIN(π/2) = 1
        SIN(π) = 0
    """

    name = "SIN"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class CosFunction(BasicFunction):
    """
    Implements the BASIC 'COS' function.

    Calculates the cosine of an angle in radians.

    Args:
        x: Angle in radians

    Returns:
        Cosine of the angle

    Examples:
        COS(0) = 1
        COS(π/2) = 0
        COS(π) = -1
    """

    name = "COS"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class TanFunction(BasicFunction):
    """
    Implements the BASIC 'TAN' function.

    Calculates the tangent of an angle in radians.

    Args:
        x: Angle in radians

    Returns:
        Tangent of the angle

    Examples:
        TAN(0) = 0
        TAN(π/4) = 1
    """

    name = "TAN"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class AtnFunction(BasicFunction):
    """
    Implements the BASIC 'ATN' function.

    Calculates the arctangent of a number, returning an angle in radians.

    Args:
        x: Numeric value

    Returns:
        Arctangent of x in radians (between -π/2 and π/2)

    Examples:
        ATN(0) = 0
        ATN(1) = π/4 (approximately 0.7854)
    """

    name = "ATN"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM


class RndFunction(BasicFunction):
    """
    Implements the BASIC 'RND' function.

    Generates a pseudo-random number between 0 and 1.
    The argument controls the behavior:
    - If arg > 0: Returns the next random number in sequence
    - If arg = 0: Returns the last random number (repeatable)
    - If arg < 0: Seeds the generator with the value and returns a deterministic result

    Args:
        x: Control value (positive, zero, or negative)

    Returns:
        Random number between 0 and 1

    Examples:
        RND(1) = 0.123... (a random number)
        RND(0) = 0.123... (same as previous call)
        RND(-13) = 0.456... (deterministic based on seed -13)
    """

    name = "RND"
    arity = 1
    arg_types = [Type.NUM]
    return_type = Type.NUM
