import pytest
from c64basic_compiler.compiler.parser import parse
from c64basic_compiler.common.basic_tokens import SUPPORTED_COMMANDS


class TestParser:
    def test_parse_simple_statement(self):
        """Test parsing a simple BASIC statement"""
        tokens = [(10, ["PRINT", "HELLO"])]

        ast = parse(tokens)

        # Check AST structure
        assert len(ast) == 1
        assert ast[0]["line"] == 10
        assert ast[0]["command"] == "PRINT"
        assert ast[0]["args"] == ["HELLO"]

    def test_parse_multiple_statements(self):
        """Test parsing multiple BASIC statements"""
        tokens = [(10, ["PRINT", "HELLO"]), (20, ["GOTO", "10"])]

        ast = parse(tokens)

        # Check AST structure
        assert len(ast) == 2
        assert ast[0]["line"] == 10
        assert ast[0]["command"] == "PRINT"
        assert ast[1]["line"] == 20
        assert ast[1]["command"] == "GOTO"
        assert ast[1]["args"] == ["10"]

    def test_parse_negative_numbers(self):
        """Test parsing statements with negative numbers"""
        tokens = [(30, ["LET", "A", "=", "-", "5"])]

        ast = parse(tokens)

        # Check numbers are properly combined
        assert ast[0]["args"] == ["A", "=", "-5"]

    def test_parse_implicit_let(self):
        """Test parsing implicit LET statements"""
        tokens = [(40, ["X", "=", "10"])]

        ast = parse(tokens)

        # Check command is converted to LET
        assert ast[0]["command"] == "LET"
        assert ast[0]["args"] == ["X", "=", "10"]

    def test_parse_if_then(self):
        """Test parsing IF statements"""
        tokens = [(50, ["IF", "A", "=", "10", "THEN", "PRINT", "YES"])]

        ast = parse(tokens)

        # IF statements should preserve their structure
        assert ast[0]["command"] == "IF"
        assert "THEN" in ast[0]["args"]
        assert "PRINT" in ast[0]["args"]

    def test_parse_empty_line(self):
        """Test parsing empty line"""
        tokens = [(60, [])]

        ast = parse(tokens)

        # Empty lines should be skipped
        assert len(ast) == 0
