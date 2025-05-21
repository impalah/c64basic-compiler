import os
import pytest
import tempfile
import shutil
from unittest.mock import patch, mock_open
from c64basic_compiler.bas2prg import (
    tokenize_line,
    convert_bas_to_prg,
    main,
    basic_tokens,
)


class TestBas2Prg:
    def setup_method(self):
        # Create temporary test directory
        self.test_dir = tempfile.mkdtemp()
        self.input_path = os.path.join(self.test_dir, "input.bas")
        self.output_path = os.path.join(self.test_dir, "output.prg")

    def teardown_method(self):
        # Remove temporary directory and files
        shutil.rmtree(self.test_dir)

    def test_tokenize_line_simple(self):
        """Test tokenizing a simple BASIC line"""
        line = '10 PRINT "HELLO"'
        result = tokenize_line(line)

        # Verify it's a bytearray
        assert isinstance(result, bytearray)
        # Line number is stored as 2 bytes
        assert result[0:2] == bytes([10, 0])
        # PRINT token should be in the output
        assert basic_tokens["PRINT"] in result

    def test_tokenize_line_with_multiple_tokens(self):
        """Test tokenizing a line with multiple tokens"""
        line = '20 IF A=10 THEN PRINT "EQUAL"'
        result = tokenize_line(line)

        assert isinstance(result, bytearray)
        assert result[0:2] == bytes([20, 0])
        assert basic_tokens["IF"] in result
        assert basic_tokens["THEN"] in result
        assert basic_tokens["PRINT"] in result

    def test_tokenize_line_with_quotes(self):
        """Test tokenizing a line with quoted strings"""
        line = '30 PRINT "DON\'T TOKENIZE "INSIDE" QUOTES"'
        result = tokenize_line(line)

        assert isinstance(result, bytearray)
        # Verify that 'PRINT' is tokenized
        assert basic_tokens["PRINT"] in result
        # But verify that quoted text is left as-is
        assert ord("D") in result
        assert ord("Q") in result
        assert ord("S") in result

    @patch(
        "builtins.open", new_callable=mock_open, read_data='10 PRINT "HELLO"\n20 END\n'
    )
    @patch("os.path.isfile", return_value=True)
    def test_convert_bas_to_prg(self, mock_isfile, mock_file):
        """Test converting BASIC file to PRG"""
        with patch("builtins.print") as mock_print:
            convert_bas_to_prg(self.input_path, self.output_path, force=True)

            # Verify the function tried to write to the output file
            assert mock_file().write.call_count > 0
            # Verify success message was printed
            mock_print.assert_called_with(
                f"PRG file created successfully: {self.output_path}"
            )

    @patch("os.path.isfile", return_value=False)
    def test_convert_nonexistent_file(self, mock_isfile):
        """Test error handling for non-existent input file"""
        with patch("sys.exit") as mock_exit, patch("builtins.print") as mock_print:
            # El problema es que la función aún intenta abrir el archivo
            # a pesar de que os.path.isfile devuelve False.
            # Necesitamos hacer un test más controlado que verifique solo el flujo
            # de error y no llegue a la parte de abrir el archivo

            # Hacemos un mock para 'open' para evitar que intente abrir el archivo real
            with patch("builtins.open", mock_open()):
                # Simulamos que sys.exit termina la ejecución sin salir del test
                mock_exit.side_effect = lambda code: None

                convert_bas_to_prg("nonexistent.bas", self.output_path)

            # Verificamos que se imprimió el mensaje de error
            mock_print.assert_any_call(
                "Error: input file 'nonexistent.bas' does not exist."
            )
            # Y que se intentó salir con código 1
            mock_exit.assert_called_with(1)

    @patch("os.path.isfile", side_effect=[True, True])  # Input exists, output exists
    @patch("builtins.input", return_value="n")  # User doesn't want to overwrite
    def test_convert_output_exists_no_overwrite(self, mock_input, mock_isfile):
        """Test handling when output file exists and user doesn't want to overwrite"""
        # Mockeamos la función completa para evitar intentar abrir archivos reales
        with (
            patch(
                "c64basic_compiler.bas2prg.open",
                mock_open(read_data='10 PRINT "HELLO"\n'),
            ),
            patch("sys.exit") as mock_exit,
            patch("builtins.print") as mock_print,
        ):

            convert_bas_to_prg(self.input_path, self.output_path)

            # Verify prompt message
            assert mock_input.call_count == 1
            # Verify operation cancelled message
            mock_print.assert_any_call("Operation cancelled.")
            # Verify exit was called
            mock_exit.assert_called_with(1)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("c64basic_compiler.bas2prg.convert_bas_to_prg")
    def test_main(self, mock_convert, mock_args):
        """Test the main function"""
        # Setup the argument parser return values
        mock_args.return_value.input = "input.bas"
        mock_args.return_value.output = "output.prg"
        mock_args.return_value.force = False

        # Call the main function
        main()

        # Verify convert_bas_to_prg was called with correct arguments
        mock_convert.assert_called_once_with("input.bas", "output.prg", False)
