"""Demo script that builds a potential, solves for eigenstates, and saves a plot showing tunneling/confinement."""

from __future__ import annotations

import argparse
import numpy as np
import matplotlib
# Use Agg backend to allow saving figures without a display
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from simulator import solve_schrodinger, finite_well_potential, double_well_potential


def run_demo(output: str = 'demo_output.png', double_well: bool = False):
    # grid
    L = 20e-9  # 20 nm total
    N = 2000
    x = np.linspace(-L / 2, L / 2, N)
    dx = x[1] - x[0]

    if double_well:
        V = double_well_potential(x, well_width=6e-9, separation=8e-9, barrier_height=0.3)
        title = 'Double well (tunneling)'
    else:
        V = finite_well_potential(x, well_width=8e-9, well_center=0.0, barrier_height=0.3)
        title = 'Single finite well (confinement)'

    energies, psi = solve_schrodinger(V, dx, mass=0.067, num_states=6)  # effective mass example (GaAs ~0.067 m_e)

    plt.figure(figsize=(8, 5))
    plt.plot(x * 1e9, V, color='k', label='V (eV)')

    # plot eigenfunctions scaled and offset by their energies
    for n in range(min(5, psi.shape[1])):
        psi_n = psi[:, n]
        # scale for visibility
        scaled = psi_n * 0.1 + energies[n]
        plt.plot(x * 1e9, scaled, label=f'n={n}, E={energies[n]:.3f} eV')

    plt.xlabel('x (nm)')
    plt.ylabel('Energy / wavefunction (eV)')
    plt.title(title)
    plt.legend(loc='upper right', fontsize='small')
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    print(f"Saved demo plot to {output}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quantum well demo')
    parser.add_argument('--output', '-o', default='demo_output.png', help='Output image file')
    parser.add_argument('--double', action='store_true', help='Use double well')
    args = parser.parse_args()
    run_demo(output=args.output, double_well=args.double)
