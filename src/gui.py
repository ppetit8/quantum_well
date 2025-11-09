"""A simple Tkinter GUI to visualize the 1D quantum well simulator.

Controls:
- single / double well
- well width (nm)
- barrier height (eV)
- separation (nm) (double well only)
- effective mass (m*/m_e)
- number of states to show

Run -> recomputes eigenstates and redraws the matplotlib canvas.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
# Use TkAgg backend for embedding
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from src.simulator import (
    solve_schrodinger,
    finite_well_potential,
    double_well_potential,
)


class QuantumWellGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Quantum well visualizer')
        self._build_ui()

    def _build_ui(self):
        # Left: controls
        ctrl = ttk.Frame(self)
        ctrl.pack(side='left', fill='y', padx=6, pady=6)

        # well type
        self.well_type = tk.StringVar(value='single')
        ttk.Label(ctrl, text='Well type').pack(anchor='w')
        ttk.Radiobutton(ctrl, text='Single well', variable=self.well_type, value='single').pack(anchor='w')
        ttk.Radiobutton(ctrl, text='Double well', variable=self.well_type, value='double').pack(anchor='w')

        # well width slider
        self.well_width = tk.DoubleVar(value=8.0)
        ttk.Label(ctrl, text='Well width (nm)').pack(anchor='w', pady=(8, 0))
        ttk.Scale(ctrl, from_=1.0, to=20.0, variable=self.well_width, orient='horizontal').pack(fill='x')

        # barrier height
        self.barrier = tk.DoubleVar(value=0.3)
        ttk.Label(ctrl, text='Barrier height (eV)').pack(anchor='w', pady=(8, 0))
        ttk.Scale(ctrl, from_=0.0, to=1.5, variable=self.barrier, orient='horizontal').pack(fill='x')

        # separation (for double well)
        self.separation = tk.DoubleVar(value=8.0)
        ttk.Label(ctrl, text='Separation (nm)').pack(anchor='w', pady=(8, 0))
        ttk.Scale(ctrl, from_=0.0, to=30.0, variable=self.separation, orient='horizontal').pack(fill='x')

        # effective mass
        self.mass = tk.DoubleVar(value=0.067)
        ttk.Label(ctrl, text='Effective mass (m*/m_e)').pack(anchor='w', pady=(8, 0))
        ttk.Scale(ctrl, from_=0.01, to=1.0, variable=self.mass, orient='horizontal').pack(fill='x')

        # number of states
        self.num_states = tk.IntVar(value=6)
        ttk.Label(ctrl, text='Number of states').pack(anchor='w', pady=(8, 0))
        ttk.Spinbox(ctrl, from_=1, to=12, textvariable=self.num_states, width=5).pack(anchor='w')

        # run button
        ttk.Button(ctrl, text='Run', command=self._on_run).pack(fill='x', pady=(12, 0))

        # energies display
        ttk.Label(ctrl, text='Energies (eV)').pack(anchor='w', pady=(12, 0))
        self.energies_text = tk.Text(ctrl, width=20, height=10)
        self.energies_text.pack(fill='both', expand=False)

        # Right: plot
        plot_frame = ttk.Frame(self)
        plot_frame.pack(side='right', fill='both', expand=True)

        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()
        self._on_run()

    def _on_run(self):
        # build grid and potential
        L = 40e-9  # 40 nm total to give space for double wells
        N = 1500
        x = np.linspace(-L / 2, L / 2, N)
        dx = x[1] - x[0]

        well_w = float(self.well_width.get()) * 1e-9
        barrier_h = float(self.barrier.get())
        sep = float(self.separation.get()) * 1e-9

        if self.well_type.get() == 'double':
            V = double_well_potential(x, well_width=well_w, separation=sep, barrier_height=barrier_h)
            title = 'Double well'
        else:
            V = finite_well_potential(x, well_width=well_w, well_center=0.0, barrier_height=barrier_h)
            title = 'Single well'

        energies, psi = solve_schrodinger(V, dx, mass=float(self.mass.get()), num_states=int(self.num_states.get()))

        # redraw
        self.ax.clear()
        # shade well regions for clarity
        well_edges = []
        if self.well_type.get() == 'double':
            centers = [-sep / 2.0, sep / 2.0]
            half = well_w / 2.0
            for c in centers:
                well_edges.append((c - half, c + half))
        else:
            half = well_w / 2.0
            well_edges.append((-half, half))

        for i, (l, r) in enumerate(well_edges):
            # clip to plotting range
            l = max(l, x[0])
            r = min(r, x[-1])
            # label only first patch so legend isn't cluttered
            lbl = 'Well region' if i == 0 else None
            self.ax.axvspan(l * 1e9, r * 1e9, color='gray', alpha=0.12, label=lbl)

        self.ax.plot(x * 1e9, V, color='k', label='V (eV)')
        for n in range(min(6, psi.shape[1])):
            scaled = psi[:, n] * 0.1 + energies[n]
            self.ax.plot(x * 1e9, scaled, label=f'n={n}, E={energies[n]:.3f} eV')

        self.ax.set_xlabel('x (nm)')
        self.ax.set_ylabel('Energy / wavefunction (eV)')
        self.ax.set_title(title)
        self.ax.legend(loc='upper right', fontsize='small')
        self.fig.tight_layout()
        self.canvas.draw()

        # update energies text
        self.energies_text.delete('1.0', tk.END)
        for i, e in enumerate(energies):
            self.energies_text.insert(tk.END, f'{i}: {e:.6f} eV\n')


def main():
    app = QuantumWellGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
