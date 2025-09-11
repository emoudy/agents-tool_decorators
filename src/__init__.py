"""
AI Agent Framework - Source Package

This package contains the core components of the AI agent framework:
- Agent orchestration and workflow management
- Tool registration and execution
- LLM integration and response generation
- Data models and configuration
"""

__version__ = "1.0.0"
__author__ = "AI Agent Framework Team"

from .config import Config

# Export main components for easy importing
from .main import main
from .models import Goal, Prompt
from .tools import register_tool, tools, tools_by_tag

__all__ = ["main", "Prompt", "Goal", "register_tool", "tools", "tools_by_tag", "Config"]
