#!/usr/bin/env python3
"""Test runner script for uisp_mikrotik_address_list_sync."""

import sys
import subprocess
import argparse


def run_tests(test_type="all", coverage=False, verbose=False):
    """Run the test suite."""
    cmd = ["python", "-m", "pytest"]
    
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term"])
    
    if verbose:
        cmd.append("-v")
    
    print(f"Running tests: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for uisp_mikrotik_address_list_sync")
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "fast"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    exit_code = run_tests(args.type, args.coverage, args.verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
