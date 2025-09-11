# Configuration, constants, and settings.
"""
Configuration management for AI Agent Framework
Handles environment detection and configuration values.
"""

import os
from typing import Dict, Any

MODEL_NAME = "anthropic/claude-3-5-sonnet-20241022"

class ConfigMeta(type):
    """Metaclass to provide dynamic attribute access for Config."""
    
    def __getattribute__(cls, name):
        """Dynamic class attribute access for environment variables."""
        if name == 'MAX_TOKENS':
            return int(os.environ.get('MAX_TOKENS', '1024'))
        elif name == 'API_KEY':
            return os.environ.get('ANTHROPIC_API_KEY')
        elif name == 'MOCK_LLM_CALLS':
            return os.environ.get('MOCK_LLM_CALLS', 'false').lower() == 'true'
        elif name == 'TEST_TIMEOUT':
            return int(os.environ.get('TEST_TIMEOUT', '30'))
        elif name == 'VERBOSE_TESTS':
            return os.environ.get('VERBOSE_TESTS', 'false').lower() == 'true'
        else:
            return super().__getattribute__(name)

class Config(metaclass=ConfigMeta):
    """Main configuration class with environment-aware settings."""
    
    @classmethod
    def get_test_config(cls) -> Dict[str, Any]:
        """Get test-specific configuration."""
        return {
            'verbose': cls.VERBOSE_TESTS,
            'mock_llm_calls': cls.MOCK_LLM_CALLS,
            'test_timeout': cls.TEST_TIMEOUT,
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return True
    
    @classmethod
    def get_test_config(cls) -> Dict[str, Any]:
        """Get test-specific configuration."""
        return {
            'verbose': cls.VERBOSE_TESTS,
            'mock_llm_calls': cls.MOCK_LLM_CALLS,
            'test_timeout': cls.TEST_TIMEOUT,
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return True

# Test configuration helper
def get_test_config(key: str = None) -> Any:
    """Get test configuration values."""
    config = Config.get_test_config()
    if key:
        return config.get(key)
    return config