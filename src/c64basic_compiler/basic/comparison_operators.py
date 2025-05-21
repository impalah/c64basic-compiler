from c64basic_compiler.basic.basic_function import BasicFunction, Type


class EqualOperator(BasicFunction):
    """
    Implements the BASIC '=' comparison operator.

    Checks if two values are equal. Works with both numbers and strings.

    Args:
        First operand: Number or string
        Second operand: Number or string (same type as first operand)

    Returns:
        Integer 0 (False) or -1 (True)

    Examples:
        5 = 5    -> -1 (True)
        5 = 6    -> 0 (False)
        "A" = "A" -> -1 (True)
    """

    name = "="
    alias = "EQUAL"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.INT

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Equal operator works if both arguments are the same type
        # or if both are numeric types
        if args[0] == args[1]:
            return True
        if args[0] in (Type.NUM, Type.INT) and args[1] in (Type.NUM, Type.INT):
            return True
        return False


class LessThanOperator(BasicFunction):
    """
    Implements the BASIC '<' comparison operator.

    Checks if the first value is less than the second value.
    Works with both numbers and strings (lexicographical comparison).

    Args:
        First operand: Number or string
        Second operand: Number or string (same type as first operand)

    Returns:
        Integer 0 (False) or -1 (True)

    Examples:
        5 < 10   -> -1 (True)
        10 < 5   -> 0 (False)
        "A" < "B" -> -1 (True)
    """

    name = "<"
    alias = "LESS"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.INT

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Same rules as equal operator
        if args[0] == args[1]:
            return True
        if args[0] in (Type.NUM, Type.INT) and args[1] in (Type.NUM, Type.INT):
            return True
        return False


class GreaterThanOperator(BasicFunction):
    """
    Implements the BASIC '>' comparison operator.

    Checks if the first value is greater than the second value.
    Works with both numbers and strings (lexicographical comparison).

    Args:
        First operand: Number or string
        Second operand: Number or string (same type as first operand)

    Returns:
        Integer 0 (False) or -1 (True)

    Examples:
        10 > 5   -> -1 (True)
        5 > 10   -> 0 (False)
        "B" > "A" -> -1 (True)
    """

    name = ">"
    alias = "GREATER"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.INT

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Same rules as equal operator
        if args[0] == args[1]:
            return True
        if args[0] in (Type.NUM, Type.INT) and args[1] in (Type.NUM, Type.INT):
            return True
        return False


class LessThanEqualOperator(BasicFunction):
    """
    Implements the BASIC '<=' comparison operator.

    Checks if the first value is less than or equal to the second value.
    Works with both numbers and strings (lexicographical comparison).

    Args:
        First operand: Number or string
        Second operand: Number or string (same type as first operand)

    Returns:
        Integer 0 (False) or -1 (True)

    Examples:
        5 <= 5   -> -1 (True)
        5 <= 10  -> -1 (True)
        10 <= 5  -> 0 (False)
    """

    name = "<="
    alias = "LESS_EQUAL"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.INT

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Same rules as equal operator
        if args[0] == args[1]:
            return True
        if args[0] in (Type.NUM, Type.INT) and args[1] in (Type.NUM, Type.INT):
            return True
        return False


class GreaterThanEqualOperator(BasicFunction):
    """
    Implements the BASIC '>=' comparison operator.

    Checks if the first value is greater than or equal to the second value.
    Works with both numbers and strings (lexicographical comparison).

    Args:
        First operand: Number or string
        Second operand: Number or string (same type as first operand)

    Returns:
        Integer 0 (False) or -1 (True)

    Examples:
        5 >= 5   -> -1 (True)
        10 >= 5  -> -1 (True)
        5 >= 10  -> 0 (False)
    """

    name = ">="
    alias = "GREATER_EQUAL"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.INT

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Same rules as equal operator
        if args[0] == args[1]:
            return True
        if args[0] in (Type.NUM, Type.INT) and args[1] in (Type.NUM, Type.INT):
            return True
        return False


class NotEqualOperator(BasicFunction):
    """
    Implements the BASIC '<>' comparison operator.

    Checks if two values are not equal. Works with both numbers and strings.

    Args:
        First operand: Number or string
        Second operand: Number or string (same type as first operand)

    Returns:
        Integer 0 (False) or -1 (True)

    Examples:
        5 <> 6   -> -1 (True)
        5 <> 5   -> 0 (False)
        "A" <> "B" -> -1 (True)
    """

    name = "<>"
    alias = "NOT_EQUAL"
    arity = 2
    arg_types = [Type.ANY, Type.ANY]
    return_type = Type.INT

    def is_type_compatible(self, args: list[Type]) -> bool:
        # Same rules as equal operator
        if args[0] == args[1]:
            return True
        if args[0] in (Type.NUM, Type.INT) and args[1] in (Type.NUM, Type.INT):
            return True
        return False
