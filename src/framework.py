# Core agent classes and main agent logic

import json
import time
import traceback
from typing import Any, Callable, Dict, List

from .models import Goal, Prompt
from .tools import tools


class Action:
    """Represents an executable action for the agent"""

    def __init__(self, name: str, function: Callable, description: str, parameters: Dict, terminal: bool = False):
        self.name = name
        self.function = function
        self.description = description
        self.terminal = terminal
        self.parameters = parameters

    def execute(self, **args) -> Any:
        """Execute the action's function with given arguments"""
        return self.function(**args)


class ActionRegistry:
    """Registry for managing available actions"""

    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        """Register a new action"""
        self.actions[action.name] = action

    def get_action(self, name: str) -> Action:
        """Get an action by name"""
        return self.actions.get(name, None)

    def get_actions(self) -> List[Action]:
        """Get all registered actions"""
        return list(self.actions.values())


class Memory:
    """Manages conversation history and context"""

    def __init__(self):
        self.items = []

    def add_memory(self, memory: dict):
        """Add a memory item to the conversation history"""
        self.items.append(memory)

    def get_memories(self, limit: int = None) -> List[Dict]:
        """Get conversation history, optionally limited"""
        return self.items[:limit] if limit else self.items

    def copy_without_system_memories(self):
        """Return a copy without system-type memories"""
        filtered_items = [m for m in self.items if m.get("type") != "system"]
        memory = Memory()
        memory.items = filtered_items
        return memory


class Environment:
    """Handles action execution and result formatting"""

    def execute_action(self, action: Action, args: dict) -> dict:
        """Execute an action and return formatted result"""
        try:
            result = action.execute(**args)
            return self.format_result(result)
        except Exception as e:
            return {"tool_executed": False, "error": str(e), "traceback": traceback.format_exc()}

    def format_result(self, result: Any) -> dict:
        """Format action result with metadata"""
        return {"tool_executed": True, "result": result, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")}


class AgentLanguage:
    """Base class for agent communication protocols"""

    def construct_prompt(self, actions: List[Action], environment: Environment, goals: List[Goal], memory: Memory) -> Prompt:
        raise NotImplementedError("Subclasses must implement this method")

    def parse_response(self, response: str) -> dict:
        raise NotImplementedError("Subclasses must implement this method")


class AgentFunctionCallingActionLanguage(AgentLanguage):
    """Function calling implementation for agent communication"""

    def format_goals(self, goals: List[Goal]) -> List:
        """Format goals into system messages"""
        sep = "\n" + "-" * 50 + "\n"
        goal_instructions = "\n\n".join([f"{goal.name}:{sep}{goal.description}{sep}" for goal in goals])
        return [{"role": "system", "content": goal_instructions}]

    def format_memory(self, memory: Memory) -> List:
        """Format memory items into message format"""
        items = memory.get_memories()
        mapped_items = []

        for item in items:
            content = item.get("content") or json.dumps(item, indent=4)

            if item.get("type") == "assistant":
                mapped_items.append({"role": "assistant", "content": content})
            elif item.get("type") == "environment":
                mapped_items.append({"role": "user", "content": content})
            else:
                mapped_items.append({"role": "user", "content": content})

        return mapped_items

    def format_actions(self, actions: List[Action]) -> List:
        """Format actions into tool definitions"""
        return [
            {
                "type": "function",
                "function": {
                    "name": action.name,
                    "description": action.description[:1024],
                    "parameters": action.parameters,
                },
            }
            for action in actions
        ]

    def construct_prompt(self, actions: List[Action], environment: Environment, goals: List[Goal], memory: Memory) -> Prompt:
        """Construct complete prompt with goals, memory, and available tools"""
        prompt_messages = []
        prompt_messages += self.format_goals(goals)
        prompt_messages += self.format_memory(memory)

        tools = self.format_actions(actions)
        return Prompt(messages=prompt_messages, tools=tools)

    def parse_response(self, response: str) -> dict:
        """Parse agent response into structured format"""
        try:
            return json.loads(response)
        except Exception:
            return {"tool": "terminate", "args": {"message": response}}


class PythonActionRegistry(ActionRegistry):
    """Python-specific action registry that loads from global tools"""

    def __init__(self, tags: List[str] = None, tool_names: List[str] = None):
        super().__init__()
        self.terminate_tool = None

        for tool_name, tool_desc in tools.items():
            if tool_name == "terminate":
                self.terminate_tool = tool_desc
                continue

            if tool_names and tool_name not in tool_names:
                continue

            tool_tags = tool_desc.get("tags", [])
            if tags and not any(tag in tool_tags for tag in tags):
                continue

            self.register(
                Action(
                    name=tool_name,
                    function=tool_desc["function"],
                    description=tool_desc["description"],
                    parameters=tool_desc.get("parameters", {}),
                    terminal=tool_desc.get("terminal", False),
                )
            )

    def register_terminate_tool(self):
        """Register the terminate tool if available"""
        if self.terminate_tool:
            self.register(
                Action(
                    name="terminate",
                    function=self.terminate_tool["function"],
                    description=self.terminate_tool["description"],
                    parameters=self.terminate_tool.get("parameters", {}),
                    terminal=self.terminate_tool.get("terminal", False),
                )
            )
        else:
            raise Exception("Terminate tool not found in tool registry")


class Agent:
    """Main agent class that orchestrates the GAME loop"""

    def __init__(
        self,
        goals: List[Goal],
        agent_language: AgentLanguage,
        action_registry: ActionRegistry,
        generate_response: Callable[[Prompt], str],
        environment: Environment,
    ):
        self.goals = goals
        self.generate_response = generate_response
        self.agent_language = agent_language
        self.actions = action_registry
        self.environment = environment

    def construct_prompt(self, goals: List[Goal], memory: Memory, actions: ActionRegistry) -> Prompt:
        """Build prompt with current context"""
        return self.agent_language.construct_prompt(
            actions=actions.get_actions(), environment=self.environment, goals=goals, memory=memory
        )

    def get_action(self, response: str):
        """Parse response and get corresponding action"""
        invocation = self.agent_language.parse_response(response)
        action = self.actions.get_action(invocation["tool"])
        return action, invocation

    def should_terminate(self, response: str) -> bool:
        """Check if agent should terminate based on response"""
        action_def, _ = self.get_action(response)
        return action_def and action_def.terminal

    def set_current_task(self, memory: Memory, task: str):
        """Set the current task in memory"""
        memory.add_memory({"type": "user", "content": task})

    def update_memory(self, memory: Memory, response: str, result: dict):
        """Update memory with agent decision and environment response"""
        new_memories = [{"type": "assistant", "content": response}, {"type": "environment", "content": json.dumps(result)}]
        for m in new_memories:
            memory.add_memory(m)

    def prompt_llm_for_action(self, full_prompt: Prompt) -> str:
        """Get response from language model"""
        return self.generate_response(full_prompt)

    def run(self, user_input: str, memory=None, max_iterations: int = 50) -> Memory:
        """
        Execute the agent's main loop.

        Args:
            user_input: The task or question for the agent
            memory: Existing memory (optional)
            max_iterations: Maximum number of iterations

        Returns:
            Memory object containing conversation history
        """
        memory = memory or Memory()
        self.set_current_task(memory, user_input)

        for iteration in range(max_iterations):
            print(f"--- Iteration {iteration + 1} ---")

            # Construct prompt with current context
            prompt = self.construct_prompt(self.goals, memory, self.actions)

            print("Agent thinking...")
            # Get agent's decision
            response = self.prompt_llm_for_action(prompt)
            print(f"Agent Decision: {response}")

            # Parse and execute action
            action, invocation = self.get_action(response)
            if not action:
                print("No valid action found, terminating...")
                break

            # Execute action in environment
            result = self.environment.execute_action(action, invocation["args"])
            print(f"Action Result: {result}")

            # Update memory
            self.update_memory(memory, response, result)

            # Check for termination
            if self.should_terminate(response):
                print("Agent terminated.")
                break

        return memory
