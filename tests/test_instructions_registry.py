import pytest
from unittest.mock import MagicMock, patch
from c64basic_compiler.compiler.instructions_registry import (
    instruction_handlers,
    get_instruction_handler,
)
from c64basic_compiler.handlers.print_handler import PrintHandler
from c64basic_compiler.handlers.let_handler import LetHandler
from c64basic_compiler.handlers.if_handler import IfHandler
from c64basic_compiler.handlers.end_handler import EndHandler


class TestInstructionsRegistry:
    def setup_method(self):
        self.mock_context = MagicMock()

    def test_instruction_handlers_registry(self):
        """Test the instruction handlers registry contains expected entries"""
        # Check a sample of expected handlers
        assert "PRINT" in instruction_handlers
        assert "LET" in instruction_handlers
        assert "IF" in instruction_handlers
        assert "FOR" in instruction_handlers
        assert "NEXT" in instruction_handlers
        assert "GOTO" in instruction_handlers
        assert "END" in instruction_handlers

        # Check handler classes are correct
        assert instruction_handlers["PRINT"] == PrintHandler
        assert instruction_handlers["LET"] == LetHandler
        assert instruction_handlers["IF"] == IfHandler
        assert instruction_handlers["END"] == EndHandler

    def test_get_instruction_handler_print(self):
        """Test getting PrintHandler"""
        instruction = {"command": "PRINT", "args": ["HELLO"], "line": 10}

        # Get handler
        handler = get_instruction_handler(instruction, self.mock_context)

        # Check correct handler type
        assert isinstance(handler, PrintHandler)

    def test_get_instruction_handler_let(self):
        """Test getting LetHandler"""
        instruction = {"command": "LET", "args": ["A", "=", "5"], "line": 20}

        # Get handler
        handler = get_instruction_handler(instruction, self.mock_context)

        # Check correct handler type
        assert isinstance(handler, LetHandler)

    def test_get_instruction_handler_case_insensitive(self):
        """Test handler lookup is case-insensitive"""
        instruction = {"command": "print", "args": ["HELLO"], "line": 10}

        # Get handler for lowercase command
        handler = get_instruction_handler(instruction, self.mock_context)

        # Should still get PrintHandler
        assert isinstance(handler, PrintHandler)

    def test_get_instruction_handler_unknown(self):
        """Test error handling for unknown command"""
        instruction = {"command": "UNKNOWN", "args": [], "line": 30}

        # Attempt to get handler for unknown command
        with pytest.raises(Exception) as excinfo:
            get_instruction_handler(instruction, self.mock_context)

        # Check error message
        assert "Unknown command 'UNKNOWN'" in str(excinfo.value)
