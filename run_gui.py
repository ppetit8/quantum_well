"""Run the GUI from the project root so package imports work.

Usage:
    python run_gui.py

This avoids the common `ModuleNotFoundError: No module named 'src'` which happens
when running `python src/gui.py` directly because the script's folder is placed
on sys.path instead of the project root.
"""
from __future__ import annotations

from src.gui import main


if __name__ == '__main__':
    main()
