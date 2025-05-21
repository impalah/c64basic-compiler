import pytest
from c64basic_compiler.common.compile_context import CompileContext


class TestCompileContext:
    def setup_method(self):
        self.context = CompileContext()

    def test_init_defaults(self):
        """Test initialization with default values"""
        # Check default properties
        assert self.context.symbol_table is not None
        assert self.context.label_counter == 0
        assert self.context.loop_stack == []
        assert self.context.string_area is not None

    def test_new_label(self):
        """Test generating new unique labels"""
        label1 = self.context.new_label()
        label2 = self.context.new_label()

        # Check labels are unique
        assert label1 != label2
        # Check label counter was incremented
        assert self.context.label_counter == 2

    def test_push_pop_loop(self):
        """Test pushing and popping values from loop stack"""
        # Push a value
        self.context.loop_stack.append("LOOP1")

        # Check value was added
        assert len(self.context.loop_stack) == 1
        assert self.context.loop_stack[0] == "LOOP1"

        # Pop the value
        value = self.context.loop_stack.pop()

        # Check correct value was popped
        assert value == "LOOP1"
        assert len(self.context.loop_stack) == 0

    def test_str_representation(self):
        """Test string representation via the as_dict method"""
        # Convert to string
        str_rep = str(self.context)

        # Check the string contains expected information
        assert "symbol_table" in str_rep
        assert "label_counter" in str_rep
        assert "loop_stack" in str_rep
        assert "string_area" in str_rep
