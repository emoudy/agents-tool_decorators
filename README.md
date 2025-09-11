## Project Overview
This agent framework builds AI agents with tool integration using Claude. It supports tool decorators, modular design, and easy extension for custom workflows.

## Directory Structure
```
src/                   # Source code package
├── __init__.py        # Package initialization and exports
├── main.py            # Main entry point and orchestrator
├── config.py          # Configuration and environment settings
├── models.py          # Data structures and type definitions
├── llm.py             # LLM interaction logic
├── framework.py       # Core agent logic and orchestration
└── tools.py           # Tool decorators and tool definitions

tests/                 # Test suite
├── __init__.py        # Test infrastructure and mocking setup
├── test_tools.py      # Tool registration and validation tests
├── test_framework.py  # Agent workflow and component tests
├── test_llm.py        # LLM integration tests
├── test_models.py     # Data structure tests
└── test_integration.py # End-to-end integration tests

main.py                # Application entry point
requirements.txt       # Python dependencies
README.md              # Project documentation
```

## Running the Application

1. **Set up your environment variables**:
   Create a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the agent**:
   ```bash
   python main.py
   ```

## Testing

The project includes a comprehensive test suite covering all modules:

### Running Tests

1. **Run all tests**:
   ```bash
   python3 -m unittest discover tests/
   ```

2. **Run specific test modules**:
   ```bash
   # Test tool functionality
   python3 -m unittest tests.test_tools
   
   # Test framework components
   python3 -m unittest tests.test_framework
   
   # Test LLM integration
   python3 -m unittest tests.test_llm
   
   # Test data models
   python3 -m unittest tests.test_models
   
   # Test integration scenarios
   python3 -m unittest tests.test_integration
   ```

3. **Run tests with verbose output**:
   ```bash
   python3 -m unittest discover tests/ -v
   ```

### Test Structure

The test suite is organized to mirror the source structure:

- `tests/__init__.py` - Test infrastructure, automatic mocking setup, and configuration
- `tests/test_tools.py` - Tool registration, validation, and decorator functionality  
- `tests/test_framework.py` - Agent workflow, memory, actions, and environment
- `tests/test_llm.py` - LLM response generation and API integration
- `tests/test_models.py` - Data structures and type definitions
- `tests/test_integration.py` - End-to-end system integration tests

All tests use automatic LLM mocking in test environments and include comprehensive coverage of the framework components.

## Troubleshooting

If you encounter issues with dependencies or environment setup:

```bash
# Remove existing virtual environment
rm -rf .venv

# Create new virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies from requirements file
pip install -r requirements.txt
```


