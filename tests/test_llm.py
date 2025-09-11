"""
Tests for LLM module - response generation and API integration.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Import from the tests package to get automatic setup
from tests import BaseTestCase, create_mock_llm_response, create_mock_tool_call, Config
from models import Prompt

# Try to import llm module, handle gracefully if missing
try:
    from llm import generate_response
    LLM_MODULE_AVAILABLE = True
except ImportError:
    LLM_MODULE_AVAILABLE = False
    # Create a dummy function for testing
    def generate_response(prompt, tools=None):
        return "Mock response for testing"


class TestGenerateResponse(BaseTestCase):
    """Test generate_response function with automatic LLM mocking."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()  # Important: call parent setUp for mocking
        self.test_prompt = Prompt(
            messages=[{"role": "user", "content": "Hello, how are you?"}],
            tools=[],
            metadata={}
        )
    
    @unittest.skipUnless(LLM_MODULE_AVAILABLE, "LLM module not available")
    def test_generate_response_basic(self):
        """Test basic response generation with automatic mocking."""
        # BaseTestCase automatically sets up mocking
        result = generate_response(self.test_prompt)
        
        # Verify we got a response
        self.assertIsNotNone(result)
        
        # Verify the mock was called
        self.mock_completion.assert_called_once()
    
    @unittest.skipUnless(LLM_MODULE_AVAILABLE, "LLM module not available")
    def test_generate_response_with_tools(self):
        """Test response generation with tool calling using automatic mocking."""
        # Create mock tools
        mock_tools = [
            {
                "type": "function",
                "function": {
                    "name": "test_tool",
                    "description": "A test tool",
                    "parameters": {}
                }
            }
        ]
        
        # Create a prompt with tools
        test_prompt_with_tools = Prompt(
            messages=[{"role": "user", "content": "Test prompt"}],
            tools=mock_tools
        )
        
        # Set up the mock response using the inherited method
        self.set_mock_llm_response("I'll help you with that.")
        
        result = generate_response(test_prompt_with_tools)
        
        # Verify the completion was called
        self.mock_completion.assert_called_once()
        
        # Verify we got a result
        self.assertIsNotNone(result)
    
    @unittest.skipUnless(LLM_MODULE_AVAILABLE, "LLM module not available")
    def test_generate_response_with_tool_calls(self):
        """Test response generation when tool calls are returned."""
        # Create a mock tool call using the utility function
        mock_tool_call = create_mock_tool_call("test_function", {"param": "value"})
        
        # Set up the mock response with tool calls
        self.set_mock_llm_response("I'll use a tool to help.", [mock_tool_call])
        
        mock_tools = [
            {
                "type": "function",
                "function": {
                    "name": "test_function",
                    "description": "A test function",
                    "parameters": {}
                }
            }
        ]
        
        # Create a prompt with tools
        test_prompt_with_tools = Prompt(
            messages=[{"role": "user", "content": "Test prompt"}],
            tools=mock_tools
        )
        
        result = generate_response(test_prompt_with_tools)
        
        # Verify we got a result
        self.assertIsNotNone(result)
        
        # Verify the mock was called
        self.mock_completion.assert_called_once()
    
    def test_prompt_structure(self):
        """Test that prompts have correct structure."""
        prompt_with_messages = Prompt(
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"}
            ],
            tools=[{"name": "test_tool", "description": "A test tool"}],
            metadata={"model": "claude-3-5-sonnet"}
        )
        
        # Verify the Prompt structure
        self.assertIsInstance(prompt_with_messages.messages, list)
        self.assertIsInstance(prompt_with_messages.tools, list)
        self.assertIsInstance(prompt_with_messages.metadata, dict)
        self.assertEqual(len(prompt_with_messages.messages), 2)
        self.assertEqual(len(prompt_with_messages.tools), 1)
    
    @unittest.skipUnless(LLM_MODULE_AVAILABLE, "LLM module not available")
    def test_custom_mock_response(self):
        """Test setting custom mock responses."""
        # Set a custom mock response
        custom_content = "This is a custom test response"
        self.set_mock_llm_response(custom_content)
        
        result = generate_response(self.test_prompt)
        
        # Verify the custom response was used
        self.assertIsNotNone(result)
        
        # Check that our mock was set up correctly
        mock_response = self.mock_completion.return_value
        self.assertEqual(mock_response.choices[0].message.content, custom_content)
    
    @unittest.skipUnless(LLM_MODULE_AVAILABLE, "LLM module not available")
    def test_api_error_handling(self):
        """Test handling of API errors."""
        # Check if mock is available
        if not hasattr(self, 'mock_completion'):
            self.skipTest("Mock completion not available")
        
        # Make the mock raise an exception
        self.mock_completion.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            generate_response(self.test_prompt)

class TestMockingInfrastructure(BaseTestCase):
    """Test that the mocking infrastructure works correctly."""
    
    def test_config_mock_setting(self):
        """Test that LLM mocking is enabled in test environment."""
        # Debug the configuration values
        print(f"Config.MOCK_LLM_CALLS: {Config.MOCK_LLM_CALLS}")
        print(f"Environment variable MOCK_LLM_CALLS: {os.environ.get('MOCK_LLM_CALLS')}")
        print(f"sys.modules with 'tests': {[m for m in sys.modules.keys() if 'tests' in m]}")
        
        self.assertTrue(Config.MOCK_LLM_CALLS)
    
    def test_mock_llm_response_creation(self):
        """Test creating mock LLM responses."""
        mock_response = create_mock_llm_response("Test response")
        
        self.assertIsNotNone(mock_response)
        self.assertIsNotNone(mock_response.choices)
        self.assertEqual(mock_response.choices[0].message.content, "Test response")
    
    def test_mock_tool_call_creation(self):
        """Test creating mock tool calls."""
        mock_tool_call = create_mock_tool_call("add", {"a": 5, "b": 3})
        
        self.assertIsNotNone(mock_tool_call)
        self.assertEqual(mock_tool_call.function.name, "add")
        self.assertIn("5", mock_tool_call.function.arguments)
        self.assertIn("3", mock_tool_call.function.arguments)
    
    def test_base_test_case_setup(self):
        """Test that BaseTestCase sets up mocking correctly."""
        # Verify that we have a mock set up
        self.assertTrue(hasattr(self, 'mock_completion'))
        self.assertIsNotNone(self.mock_completion)
        
        # Verify that Config indicates mocking is enabled
        self.assertTrue(Config.MOCK_LLM_CALLS)


class TestPromptDataStructure(BaseTestCase):
    """Test Prompt dataclass structure compatibility with LLM calls."""
    
    def test_empty_prompt_creation(self):
        """Test creating an empty prompt with defaults."""
        prompt = Prompt()
        
        self.assertEqual(prompt.messages, [])
        self.assertEqual(prompt.tools, [])
        self.assertEqual(prompt.metadata, {})
    
    def test_prompt_with_conversation_history(self):
        """Test prompt with message history."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What's the weather like?"},
            {"role": "assistant", "content": "I don't have access to weather data."},
            {"role": "user", "content": "Can you help me with math?"}
        ]
        
        prompt = Prompt(messages=messages)
        
        self.assertEqual(len(prompt.messages), 4)
        self.assertEqual(prompt.messages[0]["role"], "system")
        self.assertEqual(prompt.messages[-1]["role"], "user")
    
    def test_prompt_with_tools_metadata(self):
        """Test prompt with tools and metadata."""
        tools = [
            {"name": "calculator", "description": "Perform calculations"},
            {"name": "weather", "description": "Get weather information"}
        ]
        
        metadata = {
            "model": "claude-3-5-sonnet",
            "temperature": 0.7,
            "max_tokens": 1024
        }
        
        prompt = Prompt(tools=tools, metadata=metadata)
        
        self.assertEqual(len(prompt.tools), 2)
        self.assertEqual(prompt.metadata["model"], "claude-3-5-sonnet")
        self.assertEqual(prompt.metadata["temperature"], 0.7)


if __name__ == '__main__':
    unittest.main()