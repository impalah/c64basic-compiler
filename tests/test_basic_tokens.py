import pytest
from c64basic_compiler.common.basic_tokens import *


class TestBasicTokens:
    def test_basic_tokens_values(self):
        """Test that basic tokens have the expected values"""
        # Test a selection of tokens
        assert END == 0x80
        assert FOR == 0x81
        assert NEXT == 0x82
        assert PRINT == 0x99
        assert RETURN == 0x8E
        assert REM == 0x8F
        assert IF == 0x8B
        assert GOTO == 0x89
        assert GOSUB == 0x8D

    def test_relational_operators(self):
        """Test relational operators have correct values"""
        assert EQUAL == 0xB2
        assert GREATER == 0xB1
        assert LESS == 0xB3

    def test_arithmetic_operators(self):
        """Test arithmetic operators have correct values"""
        assert PLUS == 0xAA
        assert MINUS == 0xAB
        assert MULTIPLY == 0xAC
        assert DIVIDE == 0xAD
        assert POWER == 0xAE

    def test_logical_operators(self):
        """Test logical operators have correct values"""
        assert AND == 0xAF
        assert OR == 0xB0
        assert NOT == 0xA8

    def test_functions(self):
        """Test function tokens have correct values"""
        assert SGN == 0xB4
        assert INT == 0xB5
        assert ABS == 0xB6
        # SQR token value is actually 0xBA (186 decimal), not 0xBA (186 decimal)
        assert SQR == 0xBA  # 186 decimal
        assert RND == 0xBB
        assert SIN == 0xBF
        assert STR_DOLLAR == 0xC4

    def test_control_flow_tokens(self):
        """Test control flow tokens have correct values"""
        assert THEN == 0xA7
        assert TO == 0xA4
        assert STEP == 0xA9

    def test_io_tokens(self):
        """Test IO related tokens have correct values"""
        assert INPUT == 0x85
        assert PRINT == 0x99
        assert GET == 0xA1
        assert OPEN == 0x9F
        assert CLOSE == 0xA0

    def test_supplementary_tokens(self):
        """Test that supplementary/special tokens have correct values"""
        assert TAB_OPEN == 0xA3
        assert SPC_OPEN == 0xA6
        assert PRINT_HASH == 0x98
