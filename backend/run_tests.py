"""
Test Runner for NEXIS Platform
Run all tests with detailed output
"""
import sys
import pytest


def run_all_tests():
    """Run all tests with verbose output"""
    print("=" * 70)
    print("NEXIS Platform - Rule-Based System Test Suite")
    print("=" * 70)
    print()
    
    # Run tests with verbose output and coverage
    args = [
        'tests/',
        '-v',  # Verbose
        '--tb=short',  # Short traceback format
        '--color=yes',  # Colored output
        '-ra',  # Show summary of all test outcomes
    ]
    
    exit_code = pytest.main(args)
    
    print()
    print("=" * 70)
    if exit_code == 0:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    
    return exit_code


def run_specific_module(module_name):
    """Run tests for a specific module"""
    print(f"Running tests for: {module_name}")
    print("=" * 70)
    
    args = [
        f'tests/test_{module_name}.py',
        '-v',
        '--tb=short',
        '--color=yes',
    ]
    
    return pytest.main(args)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific module
        module = sys.argv[1]
        exit_code = run_specific_module(module)
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
