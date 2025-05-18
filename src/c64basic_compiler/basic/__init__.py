"""
Package for C64 BASIC language elements and abstractions.
"""

import inspect
import sys
from typing import Dict

# Import the base class and Type enum
from c64basic_compiler.basic.basic_function import BasicFunction, Type

# Import all function modules to register their classes
from c64basic_compiler.basic.math_functions import *
from c64basic_compiler.basic.string_functions import *
from c64basic_compiler.basic.operators import *
from c64basic_compiler.basic.logic_operators import *
from c64basic_compiler.basic.system_functions import *
from c64basic_compiler.basic.comparison_operators import *  # Ensure we import comparison operators


# Dynamically build the function table from all BasicFunction subclasses
def _build_function_table() -> Dict[str, BasicFunction]:
    """
    Dynamically builds a function table by discovering all BasicFunction subclasses.

    Returns:
        Dict mapping function names to instantiated function objects
    """
    function_table = {}

    # Find all BasicFunction subclasses in all imported modules
    for module_name, module in sys.modules.items():
        if module_name.startswith("c64basic_compiler.basic."):
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, BasicFunction)
                    and obj is not BasicFunction
                    and obj.name  # Only include classes with a name
                ):
                    function_table[obj.name] = obj()
                    # Print for debugging
                    print(f"Registered function: {obj.name}")

    return function_table


# The global function table
FUNCTION_TABLE = _build_function_table()

# Re-export Type enum so it can be imported from c64basic_compiler.basic
__all__ = ["FUNCTION_TABLE", "Type", "BasicFunction"]
