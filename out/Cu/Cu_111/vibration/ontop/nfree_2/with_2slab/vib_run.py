import os
import json


from ase.io import read, write
from ase.calculators.espresso import Espresso
from ase.optimize import BFGS, GPMin, BFGSLineSearch
from ase.data import (
    atomic_numbers,
    atomic_names,
    atomic_masses,
    covalent_radii,
    chemical_symbols,
)
from ase.units import *
from ase.calculators.socketio import SocketIOCalculator
from ase.vibrations import Vibrations
from ase.thermochemistry import HarmonicThermo
from ase.build import fcc111, bulk, molecule, add_adsorbate
from ase.io.trajectory import Trajectory
from ase.constraints import FixAtoms


def ase_calc(label, ecutwfc):
    kpts = (8, 8, 1)

    pseudopotentials = json.load(open("./../../../../pslibrary.json"))

    input_data = {
        "control": {
            "calculation": "scf",
            "title": label,
            "verbosity": "high",
            "outdir": "tmp",
            "prefix": label,
            "etot_conv_thr": 1e-5 * (eV / Ry),
            "forc_conv_thr": 0.01 * (eV / Ang) / (Ry / Bohr),
            "tprnfor": True,
            "tstress": False,
            "max_seconds": 86000,
            # "pseudo": "/home/k0227/k022716/QE/pseudo/",
        },
        "system": {
            "ecutwfc": ecutwfc,
            "ecutrho": ecutwfc * 10,
            "occupations": "smearing",
            "smearing": "marzari-vanderbilt",
            "degauss": 0.1 * (eV / Ry),
            "nosym": True,
            "noinv": True,
            "input_dft": "beef-vdw",
            "assume_isolated": "esm",
            "esm_bc": "bc3",
            "esm_w": 0,
        },
        "electrons": {
            "electron_maxstep": 9000,
            "scf_must_converge": True,
            "conv_thr": 1.0e-10 * (eV / Ry),
            "mixing_beta": 1 / 3,
            "mixing_ndim": 12,
            "mixing_mode": "plain",
            "diagonalization": "david",
        },
    }

    return Espresso(
        input_data=input_data,
        pseudopotentials=pseudopotentials,
        kpts=kpts,
        label=label,
    )


ecutwfc = 850 * (eV / Ry)

slab_structure = read("relaxed.pwo", index=-1)
constrain_bottom_layer = FixAtoms(indices=[i for i in range(9)])
slab_structure.set_constraint(constrain_bottom_layer)
structure_trajectory = Trajectory("initial-structure.traj", "w")
structure_trajectory.write(slab_structure)

user_prefix = "Cu"

calc = ase_calc(label=user_prefix + "-vib", ecutwfc=ecutwfc)
slab_structure.calc = calc
potentialenergy = slab_structure.get_potential_energy()

vib = Vibrations(slab_structure, indices=[-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20], nfree=2)
vib.run()
vib.summary(log="vibrational-frequencies.txt")
vib.write_mode()
vib_energies = vib.get_energies()
vib_frequencies = vib.get_frequencies()
thermo = HarmonicThermo(vib_energies=vib_energies, potentialenergy=potentialenergy)
T_ambient = 298.15
U = thermo.get_internal_energy(temperature=T_ambient)
S = thermo.get_entropy(temperature=T_ambient)
A = thermo.get_helmholtz_energy(temperature=T_ambient)
with open("helmholtz", "w") as helmholtz_file:
    helmholtz_file.write(str(A))
