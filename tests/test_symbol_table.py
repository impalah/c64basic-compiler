import pytest
from c64basic_compiler.common.symbol_table import SymbolTable


class TestSymbolTable:
    def setup_method(self):
        self.base_address = 0xC000
        self.symbol_table = SymbolTable(self.base_address)

    def test_init(self):
        """Test initialization with minimal assertions"""
        # Solo verificamos lo que podemos asumir con seguridad
        assert hasattr(self.symbol_table, "base_address")
        assert self.symbol_table.base_address == self.base_address

    def test_get_address(self):
        """Test get_address method"""
        # Solo probamos el método get_address que sabemos que existe
        with pytest.raises(Exception):
            # Debería fallar para una variable inexistente
            self.symbol_table.get_address("NONEXISTENT")

    def test_str_representation(self):
        """Test string representation"""
        # Solo verificamos que la representación de cadena funciona
        str_rep = str(self.symbol_table)

        # Verificamos que contiene algún texto
        assert len(str_rep) > 0
        assert "SymbolTable" in str_rep
