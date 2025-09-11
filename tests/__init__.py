"""
Tests package for AI Agent Framework
This is configuration-driven testing with automatic mocking.

This package contains comprehensive tests for all components of the agent framework:
- test_tools.py: Tool registration, validation, and decorator functionality
- test_framework.py: Agent workflow, memory, actions, and environment
- test_llm.py: LLM response generation and API integration  
- test_models.py: Data structures and type definitions
- test_integration.py: End-to-end system integration tests

Usage:
    # Run all tests
    python -m unittest discover tests/ -v
    
    # Run specific test module
    python -m unittest tests.test_tools -v
"""
import litellm
litellm._turn_on_debug()

# Load test environment first
from dotenv import load_dotenv
from pathlib import Path
import sys
from config import MODEL_NAME

# Load test-specific environment variables
project_root = Path(__file__).parent.parent
test_env_path = project_root / '.env.test'
load_dotenv(test_env_path)

# Add the project root to Python path for imports
sys.path.insert(0, str(project_root))

# NOW we can import config (after path setup)
from config import Config, get_test_config
from unittest.mock import patch, MagicMock
import unittest

class MockLLMResponse:
    """Mock response object that mimics the structure of litellm responses."""
    
    def __init__(self, content="Test response", tool_calls=None):
        self.choices = [MagicMock()]
        self.choices[0].message = MagicMock()
        self.choices[0].message.content = content
        self.choices[0].message.tool_calls = tool_calls or []

def create_mock_llm_response(content="Mock LLM response", tool_calls=None):
    """Create a mock LLM response with the expected structure."""
    return MockLLMResponse(content, tool_calls)

def create_mock_tool_call(function_name, arguments_dict, call_id="mock_call_id"):
    """Create a mock tool call object."""
    mock_tool_call = MagicMock()
    mock_tool_call.function.name = function_name
    mock_tool_call.function.arguments = str(arguments_dict).replace("'", '"')  # JSON format
    mock_tool_call.id = call_id
    return mock_tool_call

class BaseTestCase(unittest.TestCase):
    """Base test case that automatically handles LLM mocking."""
    
    def setUp(self):
        """Set up test with automatic LLM mocking if configured."""
        super().setUp()
        if Config.MOCK_LLM_CALLS:
            # Start LLM mocking for this test
            self.llm_patcher = patch('llm.completion')
            self.mock_completion = self.llm_patcher.start()
            self.mock_completion.return_value = create_mock_llm_response()
    
    def tearDown(self):
        """Clean up test mocking."""
        if hasattr(self, 'llm_patcher'):
            self.llm_patcher.stop()
        super().tearDown()
    
    def set_mock_llm_response(self, content="Mock response", tool_calls=None):
        """Convenience method to set the mock LLM response."""
        if hasattr(self, 'mock_completion'):
            self.mock_completion.return_value = create_mock_llm_response(content, tool_calls)

# Print test configuration if verbose (module level)
if Config.VERBOSE_TESTS:
    print(f"Test Environment Configuration:")
    print(f"  MOCK_LLM_CALLS: {Config.MOCK_LLM_CALLS}")
    print(f"  TEST_TIMEOUT: {Config.TEST_TIMEOUT}")
    print(f"  MODEL_NAME: {MODEL_NAME}")

# Export commonly used items for easy import
__all__ = [
    'BaseTestCase',
    'create_mock_llm_response', 
    'create_mock_tool_call',
    'get_test_config',
    'MockLLMResponse'
]