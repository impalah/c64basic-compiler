import pytest
from c64basic_compiler.compiler.tokenizer import tokenize, tokenize_line


class TestTokenizer:
    def test_tokenize_simple_program(self):
        """Test tokenizing a simple BASIC program"""
        source = '10 PRINT "HELLO"\n' "20 GOTO 10\n"

        result = tokenize(source)

        # Check result structure
        assert len(result) == 2

        # Check first line
        assert result[0][0] == 10  # Line number
        assert result[0][1] == ["PRINT", '"HELLO"']

        # Check second line
        assert result[1][0] == 20
        assert result[1][1] == ["GOTO", "10"]

    def test_tokenize_with_colons(self):
        """Test tokenizing a line with multiple statements (colons)"""
        source = '10 PRINT "A": PRINT "B"\n'

        result = tokenize(source)

        # Should produce two entries with same line number
        assert len(result) == 2
        assert result[0][0] == 10
        assert result[0][1] == ["PRINT", '"A"']
        assert result[1][0] == 10
        assert result[1][1] == ["PRINT", '"B"']

    def test_tokenize_with_strings(self):
        """Test tokenizing with string literals"""
        source = '10 PRINT "COLONS: INSIDE: STRINGS"\n'

        result = tokenize(source)

        # Colons inside strings should be preserved
        assert len(result) == 1
        assert result[0][1] == ["PRINT", '"COLONS: INSIDE: STRINGS"']

    def test_tokenize_with_negative_numbers(self):
        """Test tokenizing with negative numbers"""
        source = "10 LET A = -5\n"

        result = tokenize(source)

        # Negative numbers should be tokenized as they are in the current implementation
        assert len(result) == 1
        assert result[0][1] == ["LET", "A", "=", "-5"]

    def test_tokenize_line_simple(self):
        """Test tokenize_line with a simple line"""
        line = 'PRINT "Hello"'

        result = tokenize_line(line)

        # Check tokens
        assert result == ["PRINT", '"Hello"']

    def test_tokenize_line_with_numbers(self):
        """Test tokenize_line with numbers"""
        line = "LET X = 42.5"

        result = tokenize_line(line)

        # Check tokens
        assert result == ["LET", "X", "=", "42.5"]

    def test_tokenize_line_with_negative(self):
        """Test tokenize_line with negative numbers"""
        line = "LET X = -10"

        result = tokenize_line(line)

        # Should handle negative numbers according to the implementation
        assert result == ["LET", "X", "=", "-10"]
