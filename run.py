#!/usr/bin/env python3
"""
Entry point script to run the Mental Health Support Companion.
This script is placed at the project root to avoid import issues.
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import and run the main function
from main import main

if __name__ == "__main__":
    main()