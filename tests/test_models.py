"""
Tests for models module - data structures and type definitions.
"""
import unittest
from dataclasses import fields

# Import from the tests package to get automatic setup
from tests import BaseTestCase
from models import Prompt, Goal


class TestPrompt(BaseTestCase):
    """Test Prompt dataclass functionality."""
    
    def test_prompt_creation(self):
        """Test creating a Prompt instance."""
        prompt = Prompt(
            messages=[{"role": "user", "content": "Hello"}],
            tools=[{"name": "add", "description": "Add numbers"}],
            metadata={"model": "claude-3-5-sonnet"}
        )
        
        self.assertEqual(len(prompt.messages), 1)
        self.assertEqual(len(prompt.tools), 1)
        self.assertEqual(prompt.metadata["model"], "claude-3-5-sonnet")
    
    def test_prompt_default_values(self):
        """Test creating a Prompt with default values."""
        prompt = Prompt()  # All fields have default_factory
        
        self.assertEqual(prompt.messages, [])
        self.assertEqual(prompt.tools, [])
        self.assertEqual(prompt.metadata, {})
    
    def test_prompt_fields(self):
        """Test that Prompt has the expected fields."""
        prompt_fields = [field.name for field in fields(Prompt)]
        expected_fields = ['messages', 'tools', 'metadata']
        
        self.assertEqual(set(prompt_fields), set(expected_fields))
    
    def test_prompt_with_messages(self):
        """Test creating a Prompt with message history."""
        messages = [
            {"role": "user", "content": "Previous question"},
            {"role": "assistant", "content": "Previous answer"}
        ]
        
        prompt = Prompt(messages=messages)
        
        self.assertEqual(len(prompt.messages), 2)
        self.assertEqual(prompt.messages[0]["role"], "user")
        self.assertEqual(prompt.messages[1]["role"], "assistant")
    
    def test_prompt_with_tools(self):
        """Test creating a Prompt with tools."""
        tools = [
            {"name": "add", "description": "Add two numbers"},
            {"name": "multiply", "description": "Multiply two numbers"}
        ]
        
        prompt = Prompt(tools=tools)
        
        self.assertEqual(len(prompt.tools), 2)
        self.assertEqual(prompt.tools[0]["name"], "add")
        self.assertEqual(prompt.tools[1]["name"], "multiply")
    
    def test_prompt_mutability(self):
        """Test that Prompt fields can be modified after creation."""
        prompt = Prompt()
        
        # Add a message
        prompt.messages.append({"role": "user", "content": "Hello"})
        self.assertEqual(len(prompt.messages), 1)
        
        # Add a tool
        prompt.tools.append({"name": "test", "description": "Test tool"})
        self.assertEqual(len(prompt.tools), 1)
        
        # Add metadata
        prompt.metadata["key"] = "value"
        self.assertEqual(prompt.metadata["key"], "value")


class TestGoal(BaseTestCase):
    """Test Goal dataclass functionality."""
    
    def test_goal_creation(self):
        """Test creating a Goal instance."""
        goal = Goal(
            priority=1,
            name="Test Goal",
            description="This is a test goal"
        )
        
        self.assertEqual(goal.priority, 1)
        self.assertEqual(goal.name, "Test Goal")
        self.assertEqual(goal.description, "This is a test goal")
    
    def test_goal_fields(self):
        """Test that Goal has the expected fields."""
        goal_fields = [field.name for field in fields(Goal)]
        expected_fields = ['priority', 'name', 'description']
        
        self.assertEqual(set(goal_fields), set(expected_fields))
    
    def test_goal_immutability(self):
        """Test that Goal is frozen (immutable)."""
        goal = Goal(
            priority=1,
            name="Test Goal",
            description="Test description"
        )
        
        # Goal is frozen, so we can't modify attributes
        with self.assertRaises(AttributeError):
            goal.priority = 2
        
        with self.assertRaises(AttributeError):
            goal.name = "New Name"
    
    def test_goal_equality(self):
        """Test equality comparison between Goal instances."""
        goal1 = Goal(
            priority=1,
            name="Same Goal",
            description="Same description"
        )
        
        goal2 = Goal(
            priority=1,
            name="Same Goal",
            description="Same description"
        )
        
        self.assertEqual(goal1, goal2)
    
    def test_goal_required_fields(self):
        """Test that Goal requires all fields."""
        # Test with valid parameters
        goal = Goal(1, "Valid Name", "Valid description")
        self.assertEqual(goal.priority, 1)
        self.assertEqual(goal.name, "Valid Name")
        self.assertEqual(goal.description, "Valid description")
        
        # Test that all fields are required
        with self.assertRaises(TypeError):
            Goal()  # Missing required parameters
        
        with self.assertRaises(TypeError):
            Goal(1)  # Missing name and description
        
        with self.assertRaises(TypeError):
            Goal(1, "Only name")  # Missing description
    
    def test_goal_different_priorities(self):
        """Test Goals with different priorities."""
        goal1 = Goal(priority=1, name="High Priority", description="Important task")
        goal2 = Goal(priority=5, name="Low Priority", description="Less important task")
        
        self.assertNotEqual(goal1, goal2)
        self.assertLess(goal1.priority, goal2.priority)


class TestDataClassIntegration(BaseTestCase):
    """Test integration between dataclasses."""
    
    def test_prompt_with_goal_context(self):
        """Test using Goal information in Prompt context."""
        goal = Goal(
            priority=1,
            name="Answer Questions",
            description="Answer user questions accurately"
        )
        
        # Store goal information in prompt metadata
        metadata = {
            "goal_name": goal.name,
            "goal_description": goal.description,
            "goal_priority": goal.priority
        }
        
        prompt = Prompt(
            messages=[{"role": "system", "content": f"Your goal is: {goal.description}"}],
            metadata=metadata
        )
        
        self.assertEqual(prompt.metadata["goal_name"], goal.name)
        self.assertEqual(prompt.metadata["goal_description"], goal.description)
        self.assertIn(goal.description, prompt.messages[0]["content"])
    
    def test_multiple_goals_with_prompts(self):
        """Test creating multiple goals and associated prompts."""
        goals = [
            Goal(1, "Goal 1", "First goal description"),
            Goal(2, "Goal 2", "Second goal description"),
            Goal(3, "Goal 3", "Third goal description")
        ]
        
        prompts = []
        for goal in goals:
            prompt = Prompt(
                messages=[{"role": "system", "content": f"Working on: {goal.name}"}],
                metadata={"goal_priority": goal.priority}
            )
            prompts.append(prompt)
        
        self.assertEqual(len(goals), 3)
        self.assertEqual(len(prompts), 3)
        
        for goal, prompt in zip(goals, prompts):
            self.assertEqual(prompt.metadata["goal_priority"], goal.priority)
            self.assertIn(goal.name, prompt.messages[0]["content"])
    
    def test_prompt_tool_and_goal_integration(self):
        """Test integration of tools and goals in prompts."""
        goal = Goal(1, "Calculate", "Perform mathematical calculations")
        
        tools = [
            {"name": "add", "description": "Add two numbers"},
            {"name": "multiply", "description": "Multiply two numbers"}
        ]
        
        prompt = Prompt(
            messages=[{"role": "system", "content": f"Goal: {goal.description}"}],
            tools=tools,
            metadata={"goal_name": goal.name}
        )
        
        self.assertEqual(len(prompt.tools), 2)
        self.assertEqual(prompt.metadata["goal_name"], goal.name)
        self.assertIn(goal.description, prompt.messages[0]["content"])


if __name__ == '__main__':
    unittest.main()