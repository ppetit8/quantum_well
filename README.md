Quantum Well Simulator

A small Python package that simulates electron states in 1D quantum wells using a finite-difference Schrödinger solver. It can illustrate confinement and tunneling effects for single and double wells.

What is included

- `src/simulator.py` — finite-difference Schrödinger solver and potential builders
- `src/plot_demo.py` — demo that runs the solver and saves plots of potential and eigenstates
- `tests/test_simulator.py` — minimal tests
- `requirements.txt` — runtime dependencies

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

License: MIT
