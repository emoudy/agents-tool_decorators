# AI Agent Framework

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/agents_tool_decorators/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/agents_tool_decorators/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## Code Quality

This project enforces strict code quality standards that match the CI/CD pipeline requirements.

### Quick Quality Check

Run all quality checks locally before committing:
```bash
python quality_check.py
```

This script runs:
- **Flake8**: Linting and style checking
- **Black**: Code formatting verification  
- **isort**: Import sorting verification
- **Tests**: Full test suite execution

### Manual Quality Tools

1. **Format code with Black**:
   ```bash
   python -m black src/ tests/
   ```

2. **Sort imports with isort**:
   ```bash
   python -m isort src/ tests/
   ```

3. **Check linting with flake8**:
   ```bash
   python -m flake8 src/ --max-line-length=127
   ```

### Auto-Fix Formatting

If your code fails quality checks, you can automatically fix most issues:

```bash
# Fix all formatting and import issues in one command
python -m isort src/ tests/ && python -m black src/ tests/
```

Or run them separately:

```bash
# Fix import ordering
python -m isort src/ tests/

# Fix code formatting
python -m black src/ tests/
```

**💡 Pro Tip**: Run `python quality_check.py` after auto-fixing to verify all issues are resolved!

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

## CI/CD Pipeline

This project includes automated CI/CD using GitHub Actions:

### Workflows

1. **CI/CD Pipeline** (`.github/workflows/ci-cd.yml`):
   - Runs on every push to `main`/`develop` and all pull requests
   - Tests against Python 3.9, 3.10, 3.11, and 3.12
   - Includes linting (flake8), formatting (black), import sorting (isort)
   - Runs comprehensive test suite with coverage reporting
   - Security scanning with safety and bandit
   - Automatic documentation deployment to GitHub Pages

2. **Release Workflow** (`.github/workflows/release.yml`):
   - Triggers on version tags (e.g., `v1.0.0`)
   - Creates GitHub releases with source archives
   - Includes automated changelog generation

### Code Quality

The project enforces code quality through:
- **Black**: Code formatting (127 character line length)
- **isort**: Import sorting and organization
- **flake8**: Linting and style checking
- **pytest**: Testing with coverage reporting
- **safety**: Dependency vulnerability scanning
- **bandit**: Security linting

### Setting Up CI/CD

1. **Enable GitHub Actions**: Push to a GitHub repository to automatically trigger workflows

2. **Add Status Badges**: Update the repository URL in the README badges:
   ```markdown
   [![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions)
   ```

3. **Release Management**: Create releases by pushing version tags:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

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


