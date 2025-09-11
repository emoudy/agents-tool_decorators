"""
Integration tests for the complete agent system.
"""
import unittest
from unittest.mock import MagicMock

# Import from the tests package to get automatic setup
from tests import BaseTestCase, create_mock_llm_response, create_mock_tool_call

from main import main
from framework import Agent, PythonActionRegistry, Environment, AgentFunctionCallingActionLanguage
from models import Goal
from tools import register_tool
from config import Config
from llm import generate_response
import os


class TestAgentIntegration(BaseTestCase):
    """Test full agent integration and workflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()  # Important: calls BaseTestCase.setUp() for mocking
        self.test_goal = Goal(
            priority=1,
            name="Test Agent System",
            description="Test the agent system functionality"
        )
    
    def test_agent_basic_workflow(self):
        """Test basic agent workflow with mocked LLM response."""
        # Set up mock response using inherited method
        self.set_mock_llm_response("Hello! I understand your goal.")
        
        # Create agent components
        action_language = AgentFunctionCallingActionLanguage()
        action_registry = PythonActionRegistry()
        environment = Environment()
        
        agent = Agent([self.test_goal], action_language, action_registry, generate_response, environment)
        
        # Test that agent can be created and has expected attributes
        self.assertIsNotNone(agent.goals)
        self.assertEqual(len(agent.goals), 1)
        self.assertEqual(agent.goals[0].description, "Test the agent system functionality")
        self.assertIsNotNone(agent.environment)
    
    def test_agent_with_tool_call(self):
        """Test agent workflow with tool calling."""
        # Create a test tool
        @register_tool(description="A test tool for adding numbers")
        def test_add(a: int, b: int) -> int:
            """Add two numbers together."""
            return a + b
        
        # Create mock tool call response
        tool_call = create_mock_tool_call("test_add", {"a": 5, "b": 3})
        self.set_mock_llm_response("I'll add those numbers for you.", [tool_call])
        
        # Create agent components
        action_language = AgentFunctionCallingActionLanguage()
        action_registry = PythonActionRegistry()
        environment = Environment()
        
        agent = Agent([self.test_goal], action_language, action_registry, generate_response, environment)
        
        # Verify agent has access to registered tools
        available_actions = agent.actions.get_actions()
        action_names = [action.name for action in available_actions]
        self.assertIn("test_add", action_names)
    
    def test_tool_registration_integration(self):
        """Test that tool registration works properly."""
        @register_tool(description="Another test tool")
        def test_multiply(x: int, y: int) -> int:
            """Multiply two numbers."""
            return x * y
        
        # Create agent components
        action_language = AgentFunctionCallingActionLanguage()
        action_registry = PythonActionRegistry()
        environment = Environment()
        
        agent = Agent([self.test_goal], action_language, action_registry, generate_response, environment)
        actions = agent.actions.get_actions()
        action_names = [action.name for action in actions]
        
        self.assertIn("test_multiply", action_names)


class TestSystemConfiguration(BaseTestCase):
    """Test system configuration and setup."""
    
    def test_all_modules_importable(self):
        """Test that all modules can be imported successfully."""
        try:
            import main
            import models
            import llm
            import framework
            import tools
            import config
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")
    
    def test_config_values(self):
        """Test configuration values are properly set."""
        import config
        
        # Test that MODEL_NAME is defined
        self.assertTrue(hasattr(config, 'MODEL_NAME'))
        self.assertIsInstance(config.MODEL_NAME, str)
        self.assertTrue(len(config.MODEL_NAME) > 0)
    
    def test_dataclass_definitions(self):
        """Test that dataclasses are properly defined."""
        from models import Prompt, Goal
        from dataclasses import is_dataclass
        
        self.assertTrue(is_dataclass(Prompt))
        self.assertTrue(is_dataclass(Goal))


class TestErrorHandling(BaseTestCase):
    """Test error handling across the system."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()  # Important: calls BaseTestCase.setUp() for mocking
        self.test_goal = Goal(
            priority=1,
            name="Test Error Handling",
            description="Test error handling functionality"
        )
    
    def test_invalid_tool_parameters(self):
        """Test handling of invalid tool parameters."""
        @register_tool(description="Test tool for error handling")
        def error_prone_tool(required_param: str) -> str:
            """A tool that requires a parameter."""
            return f"Processed: {required_param}"
        
        # Create agent components
        action_language = AgentFunctionCallingActionLanguage()
        action_registry = PythonActionRegistry()
        environment = Environment()
        
        agent = Agent([self.test_goal], action_language, action_registry, generate_response, environment)
        action = agent.actions.get_action("error_prone_tool")
        
        # Execute with missing parameter - should handle gracefully
        if action:
            result = agent.environment.execute_action(action, {})
            self.assertFalse(result.get("tool_executed", False))
    
    def test_goal_validation(self):
        """Test that goals are properly validated."""
        # Test with missing required parameters should raise TypeError
        with self.assertRaises(TypeError):
            Goal()  # Missing required parameters
        
        # Test with valid parameters
        goal = Goal(priority=1, name="Valid Goal", description="Valid description")
        self.assertIsNotNone(goal.description)
        self.assertIsNotNone(goal.name)
        self.assertEqual(goal.priority, 1)

if __name__ == '__main__':
    unittest.main()