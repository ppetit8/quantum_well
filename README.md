
Quantum Well Simulator

A small, self-contained Python project that models 1D electron states in quantum wells using a finite-difference solution of the time-independent Schrödinger equation. The project demonstrates confinement and tunneling effects through single and symmetric double quantum wells. It includes a simple command-line demo, an interactive Tkinter GUI, and minimal tests.

Key features
------------
- 1D finite-difference Schrödinger solver (`src/simulator.py`) using sparse matrices from SciPy.
- Pre-built potential constructors: single finite well and symmetric double well.
- Command-line demo that saves publication-ready plots (`src/plot_demo.py`).
- Interactive Tkinter GUI (`src/gui.py` + `run_gui.py`) that lets you change well width, barrier height, separation, effective mass, and number of eigenstates; it shades the well regions and overlays eigenfunctions on the potential.
- Minimal unit tests that verify wavefunction normalization and energy ordering (`tests/test_simulator.py`).

Repo layout
-----------
- `src/simulator.py` — solver and potential builders
- `src/plot_demo.py` — headless demo that saves PNGs (uses Agg backend)
- `src/gui.py` — interactive Tkinter GUI embedding Matplotlib
- `run_gui.py` — small wrapper to run the GUI from the project root
- `tests/test_simulator.py` — basic numerical tests
- `requirements.txt` — Python dependencies
- `README.md`, `LICENSE`, `.gitignore`

Quick start
-----------
1. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the command-line demo (creates `demo_output.png` by default):

```bash
python src/plot_demo.py --output demo_output.png
```

3. Run the interactive GUI (requires a display):

```bash
# from the project root
python run_gui.py
```

Notes on running the GUI
------------------------
- If you run `python src/gui.py` directly you may see `ModuleNotFoundError: No module named 'src'` because running a script from inside `src/` changes Python's import search path. Use `python run_gui.py` (provided) or run as a module from the project root:

```bash
PYTHONPATH=. python -m src.gui
```

- On remote hosts without a display, either enable X forwarding (`ssh -X`) or use the headless demo (`src/plot_demo.py`) which uses Matplotlib's Agg backend.

Developer notes / contract
--------------------------
- Inputs: a 1D grid `x`, potential `V(x)` in eV, grid spacing `dx` (m), and effective mass (as a multiple of the electron mass).
- Outputs: eigenenergies (eV) and normalized eigenfunctions sampled on the grid (psi(x) such that sum |psi|^2 * dx = 1).
- Limitations: 1D, single-particle Schrödinger equation (no electron-electron interactions), uses uniform grid and finite differences. For very small dx or pathological potentials, numerical stability and performance depend on grid size and solver settings.

Testing and CI
--------------
- Minimal test included: `tests/test_simulator.py` (normalization + energy ordering). Run directly:

```bash
PYTHONPATH=. python tests/test_simulator.py
```

or with pytest (install `pytest` in the venv):

```bash
pip install pytest
python -m pytest -q
```

Suggested next steps (optional)
-------------------------------
- Add a GitHub Actions workflow to run tests on push.
- Add additional potentials (triangular, graded heterostructures) or support for arbitrary layer stacks with different effective masses.
- Add an export function in the GUI to save eigenstate data (CSV) and images.

License
-------
MIT

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the demo to produce a plot file:

```bash
python src/plot_demo.py --output demo_output.png
```

3. Run the GUI (interactive; requires a display):

```bash
python src/gui.py
```

License: MIT
