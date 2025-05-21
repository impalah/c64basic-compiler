import pytest
from c64basic_compiler.common.string_area import StringAreaAllocator


class TestStringAreaAllocator:
    def setup_method(self):
        self.start_address = 0xC800
        self.allocator = StringAreaAllocator(self.start_address)

    def test_init(self):
        """Test initialization with actual implementation attributes"""
        assert hasattr(self.allocator, "base")
        assert self.allocator.base == self.start_address
        assert hasattr(self.allocator, "current")
        assert self.allocator.current == self.start_address
        assert hasattr(self.allocator, "storage")
        assert isinstance(self.allocator.storage, list)
        assert len(self.allocator.storage) == 0

    def test_store_string(self):
        """Test store_string method"""
        string = "TEST STRING"

        # Store the string
        address = self.allocator.store_string(string)

        # Check address was returned
        assert isinstance(address, int)

        # Check storage contains the string
        assert len(self.allocator.storage) == 1
        stored_addr, stored_text = self.allocator.storage[0]
        assert stored_addr == self.start_address
        assert stored_text == string

        # Current address should be updated
        assert self.allocator.current == self.start_address + len(string) + 1

    def test_emit(self):
        """Test emit method"""
        string1 = "HELLO"
        string2 = "WORLD"

        # Store strings
        self.allocator.store_string(string1)
        self.allocator.store_string(string2)

        # Get binary data
        data = self.allocator.emit()

        # Verify output
        assert isinstance(data, bytearray)
        assert b"HELLO\x00WORLD\x00" in data
