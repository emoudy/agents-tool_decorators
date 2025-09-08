# Dataclasses, type hints, and data structures

from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Prompt:
    """Represents a prompt with messages and available tools"""
    messages: List[Dict] = field(default_factory=list)
    tools: List[Dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

@dataclass(frozen=True)
class Goal:
    """Represents an agent goal with priority and description"""
    priority: int
    name: str
    description: str