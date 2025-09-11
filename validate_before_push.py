#!/usr/bin/env python3
"""
Pre-push validation script for the AI Agent Framework.
Run this script before pushing code to ensure it will pass the CI/CD pipeline.
"""

import sys
import subprocess
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n🔍 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stdout:
                print(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                print(f"STDERR:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def check_environment() -> bool:
    """Check if the environment is properly set up."""
    print("\n🔧 Checking environment setup...")
    
    # Check if virtual environment exists
    venv_path = Path(__file__).parent / ".venv"
    if venv_path.exists():
        python_cmd = str(venv_path / "bin" / "python")
        print(f"✅ Using virtual environment: {python_cmd}")
    else:
        python_cmd = "python"
        print("⚠️  No virtual environment found, using system Python")
    
    # Check if requirements.txt exists
    requirements_path = Path(__file__).parent / "requirements.txt"
    if not requirements_path.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("✅ Environment check passed")
    return True


def main():
    """Run all pre-push validation checks."""
    print("🚀 AI Agent Framework - Pre-Push Validation")
    print("=" * 60)
    
    # Check environment setup
    if not check_environment():
        print("\n❌ Environment setup failed. Please fix and try again.")
        return 1
    
    # Find Python executable
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
    if venv_python.exists():
        python_cmd = str(venv_python)
    else:
        python_cmd = "python"
    
    # Define validation checks (same as CI/CD pipeline)
    checks = [
        # Core quality checks
        (f"{python_cmd} quality_check.py", 
         "Code Quality Checks (flake8, black, isort)"),
        
        # Test suite
        (f"{python_cmd} -m unittest discover tests/ -v", 
         "Unit Test Suite"),
        
        # Security checks
        (f"{python_cmd} -m safety check -r requirements.txt", 
         "Security Vulnerability Scan"),
        
        (f"{python_cmd} -m bandit -r src/ -q", 
         "Security Linting (Bandit)"),
        
        # Package validation
        (f"{python_cmd} -c \"from src import main, models, tools, config; print('All imports successful')\"", 
         "Package Import Validation"),
    ]
    
    print(f"\n📋 Running {len(checks)} validation checks...")
    
    results = []
    for command, description in checks:
        success = run_command(command, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PRE-PUSH VALIDATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description:<35} {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All validation checks passed!")
        print("✅ Your code is ready to push and will pass the CI/CD pipeline.")
        print("\n💡 You can now safely run: git push")
        return 0
    else:
        print("\n⚠️  Some validation checks failed!")
        print("❌ Please fix the issues above before pushing.")
        print("\n🔧 Quick fixes:")
        print("   - Run: python -m black src/ tests/")
        print("   - Run: python -m isort src/ tests/")
        print("   - Check the error messages above for specific issues")
        print("   - Run: python quality_check.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
