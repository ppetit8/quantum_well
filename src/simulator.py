"""Simple 1D Schrödinger solver using finite differences.

Functions:
- solve_schrodinger(V, dx, mass=1.0, num_states=6): returns eigenenergies (eV) and eigenfunctions
- finite_well_potential(x, well_width, well_center, barrier_height): create single finite well
- double_well_potential(x, well_width, separation, barrier_height): create symmetric double well

Units: x in meters, mass in units of electron mass, energies returned in eV.
"""
from __future__ import annotations

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

# physical constants
hbar = 1.054571817e-34  # J*s
m_e = 9.1093837015e-31  # kg
eV = 1.602176634e-19  # J


def solve_schrodinger(V: np.ndarray, dx: float, mass: float = 1.0, num_states: int = 6):
    """Solve 1D time-independent Schrödinger equation with finite differences.

    Args:
        V: potential array (in eV) defined on grid points.
        dx: grid spacing in meters.
        mass: effective mass in units of electron mass (m_e).
        num_states: number of lowest eigenstates to compute.

    Returns:
        energies (num_states,) in eV (sorted ascending)
        wavefuncs (N, num_states) normalized on the grid (sum |psi|^2 dx = 1)
    """
    N = V.size
    m = mass * m_e
    # Kinetic prefactor: -(hbar^2)/(2m) * d2/dx2. We'll build matrix in J, convert potentials to J.
    coeff = hbar ** 2 / (2.0 * m * dx ** 2)

    main = np.full(N, 2.0) * coeff
    off = np.full(N - 1, -1.0) * coeff

    H_kin = diags([off, main, off], offsets=[-1, 0, 1], format="csr")

    # Potential in J
    VJ = V * eV
    H = H_kin + diags(VJ, offsets=0, format="csr")

    k = min(num_states, N - 2)
    # Use eigsh to get lowest eigenvalues; shift-invert could be used but this is fine for small N
    vals, vecs = eigsh(H, k=k, sigma=None, which='SA')

    # eigsh returns eigenvalues in ascending order generally; ensure sorting
    idx = np.argsort(vals)
    vals = vals[idx]
    vecs = vecs[:, idx]

    # convert energies to eV
    energies = vals / eV

    # normalize wavefunctions
    for i in range(vecs.shape[1]):
        psi = vecs[:, i]
        norm = np.sqrt(np.sum(np.abs(psi) ** 2) * dx)
        vecs[:, i] = psi / norm

    return energies, vecs


def finite_well_potential(x: np.ndarray, well_width: float, well_center: float, barrier_height: float):
    """Create a single finite well potential.

    Potential is barrier_height (eV) outside the well and 0 inside the well. The well is centered at well_center.
    """
    V = np.full_like(x, barrier_height)
    half = well_width / 2.0
    V[np.logical_and(x >= (well_center - half), x <= (well_center + half))] = 0.0
    return V


def double_well_potential(x: np.ndarray, well_width: float, separation: float, barrier_height: float):
    """Create symmetric double well: two wells of `well_width` separated by center-to-center distance `separation`.

    Wells are at x = -separation/2 and +separation/2.
    Outside wells: barrier_height (eV), inside wells: 0.0 eV.
    """
    V = np.full_like(x, barrier_height)
    centers = [-separation / 2.0, separation / 2.0]
    half = well_width / 2.0
    for c in centers:
        mask = np.logical_and(x >= (c - half), x <= (c + half))
        V[mask] = 0.0
    return V
