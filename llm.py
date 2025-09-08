# LLM integration and response generation functions
import json

from litellm import completion
from config import MODEL_NAME
from models import Prompt


def generate_response(prompt: Prompt) -> str:
    """
    Generate a response from LLM using the provided prompt.
    Args:
        prompt: Prompt object containing messages and tools
    Returns:
        str: Response from Claude (either text or JSON for tool calls)
    """
    messages = prompt.messages
    tools = prompt.tools

    if not tools:
        response = completion(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=1024
        )
        return response.choices[0].message.content
    else:
        response = completion(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            max_tokens=1024
        )

        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            return json.dumps(result)
        else:
            return response.choices[0].message.content