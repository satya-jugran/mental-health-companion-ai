"""
Test runner script for Mental Health Support Companion
"""
import sys
import subprocess


def run_tests():
    """Run all tests using pytest"""
    print("=" * 60)
    print("Running Mental Health Support Companion Test Suite")
    print("=" * 60)
    print()
    
    # Run pytest with coverage
    try:
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short"],
            check=False
        )
        
        print()
        print("=" * 60)
        if result.returncode == 0:
            print("✓ All tests passed!")
        else:
            print("✗ Some tests failed. See output above for details.")
        print("=" * 60)
        
        return result.returncode
    
    except FileNotFoundError:
        print("Error: pytest not found. Please install it:")
        print("  pip install pytest pytest-asyncio")
        return 1


def run_specific_test(test_path):
    """Run a specific test file or test case"""
    print(f"Running specific test: {test_path}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            ["pytest", test_path, "-v", "--tb=short"],
            check=False
        )
        return result.returncode
    
    except FileNotFoundError:
        print("Error: pytest not found. Please install it:")
        print("  pip install pytest pytest-asyncio")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        exit(run_specific_test(sys.argv[1]))
    else:
        # Run all tests
        exit(run_tests())