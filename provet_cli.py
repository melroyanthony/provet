#!/usr/bin/env python3
"""Command-line wrapper for Provet Cloud Discharge Note Generator.

This is a simple wrapper script that forwards command-line arguments to the
main entry point of the application.
"""

import sys

from provet.__main__ import main

if __name__ == "__main__":
    sys.exit(main())
