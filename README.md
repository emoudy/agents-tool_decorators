## Project Overview
This agent framework builds AI agents with tool integration using Claude. It supports tool decorators, modular design, and easy extension for custom workflows.

## Directory Structure
```
main.py                # Main entry point and orchestrator
models.py              # Data structures and type definitions
llm.py                 # LLM interaction logic
framework.py           # Core agent logic and orchestration
tools.py               # Tool decorators and tool definitions
README.md              # Project documentation
```

## Setup & Run Instructions

1. **Install dependencies and set up your environment:**
	```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install python-dotenv litellm
	```

2. **Set your Anthropic API key in a `.env` file:**
	Create a file named `.env` in your project root with the content as in the `.env_example` file.

3. **Run the agent:**
	```sh
	python main.py
	```

This will start the agent and execute the workflow defined in `main.py`.

# troubleshoot
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install python-dotenv litellm


