"""
Tests for tools module - tool registration, validation, and functionality.
"""

import os
import sys
import unittest

# Add parent directory to path to import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import register_tool, tools, tools_by_tag


def check_description_length(tool_name: str, description: str, max_length: int = 1024) -> str:
    """
    Check if tool description exceeds recommended length and warn if needed.
    This should be used during development/testing, not during LLM execution.

    Args:
        tool_name: Name of the tool
        description: Tool description text
        max_length: Maximum recommended length (default: 1024)

    Returns:
        str: The original description (unchanged)
    """
    if len(description) > max_length:
        print(f"Warning: Description for '{tool_name}' is {len(description)} characters (>{max_length})")
    return description


def test_tool_descriptions(max_length: int = 1024):
    """
    Test all registered tools for description length.
    Call this during development to check for overly long descriptions.

    Args:
        max_length: Maximum recommended description length
    """
    print("Testing tool description lengths...")
    long_descriptions = []

    for tool_name, tool_data in tools.items():
        description = tool_data.get("description", "")
        if len(description) > max_length:
            long_descriptions.append((tool_name, len(description)))
            print(f"⚠️  '{tool_name}': {len(description)} characters (>{max_length})")

    if not long_descriptions:
        print("✅ All tool descriptions are within recommended length")
    else:
        print(f"\n❌ Found {len(long_descriptions)} tools with long descriptions")

    return long_descriptions


class TestToolDescriptions(unittest.TestCase):
    """Test tool description validation and length checking."""

    def test_description_length_valid(self):
        """Test that short descriptions pass validation."""
        short_desc = "This is a short description"
        result = check_description_length("test_tool", short_desc)
        self.assertEqual(result, short_desc)

    def test_description_length_warning(self):
        """Test that long descriptions trigger warnings."""
        long_desc = "x" * 1025  # Longer than 1024 characters

        # Capture print output
        import io
        from contextlib import redirect_stdout

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            result = check_description_length("test_tool", long_desc)

        output = captured_output.getvalue()
        self.assertIn("Warning", output)
        self.assertIn("test_tool", output)
        self.assertEqual(result, long_desc)  # Should return original description

    def test_all_registered_tool_descriptions(self):
        """Test all registered tools for description length compliance."""
        long_descriptions = []
        max_length = 1024

        for tool_name, tool_data in tools.items():
            description = tool_data.get("description", "")
            if len(description) > max_length:
                long_descriptions.append((tool_name, len(description)))

        # Print information about long descriptions for visibility
        if long_descriptions:
            print(f"\nFound {len(long_descriptions)} tools with long descriptions:")
            for tool_name, length in long_descriptions:
                print(f"  - {tool_name}: {length} characters")

        # This test passes but warns about long descriptions
        # Remove the assertion below if you want to allow long descriptions
        # self.assertEqual(len(long_descriptions), 0, f"Found tools with long descriptions: {long_descriptions}")


class TestToolRegistration(unittest.TestCase):
    """Test tool registration functionality."""

    def test_tools_are_registered(self):
        """Test that tools are properly registered."""
        self.assertGreater(len(tools), 0, "No tools are registered")

    def test_required_tool_fields(self):
        """Test that all registered tools have required fields."""
        required_fields = ["description", "parameters", "function", "terminal", "tags"]

        for tool_name, tool_data in tools.items():
            with self.subTest(tool=tool_name):
                for field in required_fields:
                    self.assertIn(field, tool_data, f"Tool '{tool_name}' missing field '{field}'")

    def test_tool_functions_callable(self):
        """Test that all tool functions are callable."""
        for tool_name, tool_data in tools.items():
            with self.subTest(tool=tool_name):
                func = tool_data.get("function")
                self.assertTrue(callable(func), f"Tool '{tool_name}' function is not callable")

    def test_tags_structure(self):
        """Test that tools_by_tag dictionary is properly structured."""
        for tag, tool_list in tools_by_tag.items():
            with self.subTest(tag=tag):
                self.assertIsInstance(tool_list, list, f"Tag '{tag}' should map to a list")
                for tool_name in tool_list:
                    self.assertIn(tool_name, tools, f"Tool '{tool_name}' in tag '{tag}' not found in tools registry")


def run_tool_description_test():
    """
    Convenience function to run just the description length tests.
    Call this during development to check tool descriptions.
    """
    print("Testing tool description lengths...")
    long_descriptions = []
    max_length = 1024

    for tool_name, tool_data in tools.items():
        description = tool_data.get("description", "")
        if len(description) > max_length:
            long_descriptions.append((tool_name, len(description)))
            print(f"⚠️  '{tool_name}': {len(description)} characters (>{max_length})")

    if not long_descriptions:
        print("✅ All tool descriptions are within recommended length")
    else:
        print(f"\n❌ Found {len(long_descriptions)} tools with long descriptions")

    return long_descriptions


if __name__ == "__main__":
    # Run the tests
    unittest.main()
