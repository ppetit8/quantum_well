import numpy as np
from src.simulator import solve_schrodinger, finite_well_potential


def test_normalization_and_ordering():
    L = 20e-9
    N = 500
    x = np.linspace(-L/2, L/2, N)
    dx = x[1] - x[0]
    V = finite_well_potential(x, well_width=8e-9, well_center=0.0, barrier_height=0.5)
    energies, psi = solve_schrodinger(V, dx, mass=0.067, num_states=4)
    # energies should be sorted ascending
    assert np.all(np.diff(energies) >= -1e-8)
    # check normalization
    for i in range(psi.shape[1]):
        norm = np.sum(np.abs(psi[:, i])**2) * dx
        assert abs(norm - 1.0) < 1e-6
