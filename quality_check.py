#!/usr/bin/env python3
"""
Quality check script for the AI Agent Framework.
Run this script to check code formatting, linting, and import sorting.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n🔍 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(
            command.split(),
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} passed")
            return True
        else:
            print(f"❌ {description} failed")
            print(f"Error output:\n{result.stdout}\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Run all quality checks."""
    print("🚀 Running AI Agent Framework Quality Checks")
    print("=" * 50)
    
    # Find Python executable
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
    if venv_python.exists():
        python_cmd = str(venv_python)
    else:
        python_cmd = "python"
    
    checks = [
        (f"{python_cmd} -m flake8 src/ --count --max-complexity=10 --max-line-length=127 --statistics", 
         "Flake8 linting"),
        (f"{python_cmd} -m black --check src/ tests/", 
         "Black code formatting"),
        (f"{python_cmd} -m isort --check-only src/ tests/", 
         "Import sorting (isort)"),
        (f"{python_cmd} -m unittest discover tests/ -v", 
         "Unit test suite"),
    ]
    
    results = []
    for command, description in checks:
        success = run_command(command, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 QUALITY CHECK SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description:<25} {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All quality checks passed! Your code is ready for CI/CD.")
        return 0
    else:
        print("\n⚠️  Some quality checks failed. Please fix the issues above.")
        print("\n💡 Quick fixes:")
        print("   - Run: python -m black src/ tests/")
        print("   - Run: python -m isort src/ tests/")
        print("   - Check flake8 output for specific issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
