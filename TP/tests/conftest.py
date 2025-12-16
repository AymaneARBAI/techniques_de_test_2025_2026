"""Pytest fixtures for triangulator tests.

This module ensures the `TP` package directory is on sys.path so tests can
import project modules (e.g. `from app import create_app`).
"""

import sys
from pathlib import Path

# Ensure the TP package directory is importable during tests
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
