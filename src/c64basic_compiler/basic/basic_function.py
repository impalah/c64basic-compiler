from enum import Enum
from typing import List, ClassVar


class Type(Enum):
    """Enumeration of supported data types in BASIC."""

    NUM = 1
    INT = 2
    STR = 3
    ANY = 4


class BasicFunction:
    """
    Base class for all BASIC functions and operators.

    All BASIC functions should inherit from this class and set their specific
    attributes for name, arity, argument types, and return type.
    """

    name: ClassVar[str] = ""
    alias: ClassVar[str] = ""
    arity: ClassVar[int] = 0
    arg_types: ClassVar[list[Type]] = []
    return_type: ClassVar[Type] = Type.ANY

    @property
    def mnemonic(self) -> str:
        """
        Get the mnemonic representation of this function.

        Returns:
            The mnemonic string for this function
        """
        return self.alias if self.alias else self.name

    def __init__(self) -> None:
        pass

    def is_type_compatible(self, args: list[Type]) -> bool:
        """
        Check if the given argument types are compatible with this function.

        Special handling for certain operators like '+' is done in subclasses.

        Args:
            args: List of argument types to check

        Returns:
            True if types are compatible, False otherwise
        """
        return all(self._compatible(a, e) for a, e in zip(args, self.arg_types))

    def resolve_return_type(self, args: list[Type]) -> Type:
        """
        Determine the return type of this function based on its declaration
        and argument types.

        Args:
            args: List of argument types

        Returns:
            The resolved return type
        """
        return args[0] if self.return_type == Type.ANY else self.return_type

    def _compatible(self, given: Type, expected: Type) -> bool:
        """
        Check if a given type is compatible with an expected type.

        Args:
            given: The provided type
            expected: The expected type

        Returns:
            True if types are compatible, False otherwise
        """
        if expected == Type.ANY:
            return True
        if expected == Type.NUM and given in (Type.NUM, Type.INT):
            return True
        if expected == Type.INT and given == Type.NUM:
            return True
        return given == expected
