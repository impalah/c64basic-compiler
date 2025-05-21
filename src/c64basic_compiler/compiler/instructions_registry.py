from c64basic_compiler.handlers.end_handler import EndHandler
from c64basic_compiler.handlers.for_handler import ForHandler
from c64basic_compiler.handlers.get_handler import GetHandler  # Add import for GET
from c64basic_compiler.handlers.gosub_handler import GosubHandler
from c64basic_compiler.handlers.goto_handler import GotoHandler
from c64basic_compiler.handlers.if_handler import IfHandler
from c64basic_compiler.handlers.input_handler import InputHandler
from c64basic_compiler.handlers.let_handler import LetHandler
from c64basic_compiler.handlers.next_handler import NextHandler
from c64basic_compiler.handlers.poke_handler import PokeHandler
from c64basic_compiler.handlers.print_handler import PrintHandler
from c64basic_compiler.handlers.rem_handler import RemHandler
from c64basic_compiler.handlers.return_handler import ReturnHandler

# Create a dictionary of handler classes
instruction_handlers = {
    "PRINT": PrintHandler,
    "GOTO": GotoHandler,
    "END": EndHandler,
    "REM": RemHandler,
    "LET": LetHandler,
    "GOSUB": GosubHandler,
    "RETURN": ReturnHandler,
    "FOR": ForHandler,
    "NEXT": NextHandler,
    "POKE": PokeHandler,
    "INPUT": InputHandler,
    "GET": GetHandler,  # Add entry for GET
}


def get_instruction_handler(instr, context):
    command = instr["command"].upper()
    handler_class = instruction_handlers.get(command)

    if handler_class is None:
        raise Exception(f"Unknown command '{command}'")

    return handler_class(instr, context)


# Import IfHandler at the end to avoid circular import

instruction_handlers["IF"] = IfHandler
