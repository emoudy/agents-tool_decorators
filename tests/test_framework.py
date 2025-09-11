"""
Tests for framework module - agent functionality, memory, actions, etc.
"""
import unittest
import sys
import os

# Add parent directory to path to import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework import Action, ActionRegistry, Memory, Environment, Agent
from models import Goal


class TestAction(unittest.TestCase):
    """Test Action class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        def dummy_function(x: int) -> int:
            return x * 2
        
        self.action = Action(
            name="test_action",
            function=dummy_function,
            description="A test action",
            parameters={"type": "object", "properties": {"x": {"type": "integer"}}},
            terminal=False
        )
    
    def test_action_creation(self):
        """Test that actions are created correctly."""
        self.assertEqual(self.action.name, "test_action")
        self.assertEqual(self.action.description, "A test action")
        self.assertFalse(self.action.terminal)
    
    def test_action_execute(self):
        """Test that actions execute correctly."""
        result = self.action.execute(x=5)
        self.assertEqual(result, 10)


class TestActionRegistry(unittest.TestCase):
    """Test ActionRegistry functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = ActionRegistry()
        
        def dummy_function():
            return "test"
        
        self.test_action = Action(
            name="test_action",
            function=dummy_function,
            description="Test action",
            parameters={}
        )
    
    def test_register_action(self):
        """Test registering actions."""
        self.registry.register(self.test_action)
        self.assertIn("test_action", self.registry.actions)
    
    def test_get_action(self):
        """Test retrieving actions."""
        self.registry.register(self.test_action)
        retrieved = self.registry.get_action("test_action")
        self.assertEqual(retrieved, self.test_action)
    
    def test_get_nonexistent_action(self):
        """Test retrieving non-existent actions."""
        result = self.registry.get_action("nonexistent")
        self.assertIsNone(result)
    
    def test_get_all_actions(self):
        """Test getting all registered actions."""
        self.registry.register(self.test_action)
        actions = self.registry.get_actions()
        self.assertEqual(len(actions), 1)
        self.assertIn(self.test_action, actions)


class TestMemory(unittest.TestCase):
    """Test Memory class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.memory = Memory()
    
    def test_add_memory(self):
        """Test adding memories."""
        memory_item = {"type": "user", "content": "Hello"}
        self.memory.add_memory(memory_item)
        self.assertEqual(len(self.memory.items), 1)
        self.assertEqual(self.memory.items[0], memory_item)
    
    def test_get_memories(self):
        """Test retrieving memories."""
        items = [
            {"type": "user", "content": "Hello"},
            {"type": "assistant", "content": "Hi there"}
        ]
        for item in items:
            self.memory.add_memory(item)
        
        memories = self.memory.get_memories()
        self.assertEqual(len(memories), 2)
        self.assertEqual(memories, items)
    
    def test_get_memories_with_limit(self):
        """Test retrieving memories with limit."""
        items = [
            {"type": "user", "content": "1"},
            {"type": "user", "content": "2"},
            {"type": "user", "content": "3"}
        ]
        for item in items:
            self.memory.add_memory(item)
        
        limited_memories = self.memory.get_memories(limit=2)
        self.assertEqual(len(limited_memories), 2)


class TestEnvironment(unittest.TestCase):
    """Test Environment class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.environment = Environment()
        
        def test_function(x: int) -> int:
            return x + 1
        
        self.test_action = Action(
            name="test_action",
            function=test_function,
            description="Test action",
            parameters={}
        )
    
    def test_execute_action_success(self):
        """Test successful action execution."""
        result = self.environment.execute_action(self.test_action, {"x": 5})
        
        self.assertTrue(result["tool_executed"])
        self.assertEqual(result["result"], 6)
        self.assertIn("timestamp", result)
    
    def test_execute_action_error(self):
        """Test action execution with error."""
        # This should cause an error (missing required argument)
        result = self.environment.execute_action(self.test_action, {})
        
        self.assertFalse(result["tool_executed"])
        self.assertIn("error", result)
        self.assertIn("traceback", result)


if __name__ == '__main__':
    unittest.main()
