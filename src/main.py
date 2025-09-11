#!/usr/bin/env python3
"""
AI Agent Framework with Claude Integration
A tool decorator system for building AI agents with Claude.
"""

import os

from dotenv import load_dotenv

from .framework import Agent, AgentFunctionCallingActionLanguage, Environment, PythonActionRegistry
from .llm import generate_response
from .models import Goal

load_dotenv()


def main():
    """Example usage of the agent framework"""
    # Set up API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Define goals
    goals = [
        Goal(
            priority=1,
            name="Helpful Assistant",
            description="You are a helpful AI assistant. Use the available tools to help users with their tasks.",
        )
    ]

    # Set up components
    language = AgentFunctionCallingActionLanguage()
    action_registry = PythonActionRegistry()
    action_registry.register_terminate_tool()
    environment = Environment()

    # Create agent
    agent = Agent(
        goals=goals,
        agent_language=language,
        action_registry=action_registry,
        generate_response=generate_response,
        environment=environment,
    )

    # Run agent
    print("Starting AI Agent with Claude...")
    memory = agent.run("Help me add 5 + 3 and then tell me about Python programming")

    print("\n--- Final Memory ---")
    for i, item in enumerate(memory.get_memories()):
        print(f"{i + 1}. {item}")


if __name__ == "__main__":
    main()
