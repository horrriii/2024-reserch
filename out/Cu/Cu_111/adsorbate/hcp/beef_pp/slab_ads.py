import os
import json
import math
import random

from ase.io import read, write
from ase.calculators.espresso import Espresso
from ase.units import *
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter
from ase.build import fcc111, bulk, add_adsorbate
from ase.io.trajectory import Trajectory
from ase.constraints import FixAtoms


def ase_calc(label, ecutwfc):
    kpts = (8, 8, 1)

    pseudopotentials = json.load(open("./pslibrary.json"))

    input_data = {
        "control": {
            "calculation": "relax",
            "title": label,
            "verbosity": "high",
            "restart_mode": "restart",
            "outdir": "tmp",
            "prefix": label,
            "etot_conv_thr": 1e-5 * (eV / Ry),
            "forc_conv_thr": 0.01 * (eV / Ang) / (Ry / Bohr),
            "tprnfor": True,
            "tstress": False,
            "max_seconds": 86000,
            "pseudo_dir": "/home/k0227/k022716/QE/pseudo/beef/",
        },
        "system": {
            "ecutwfc": ecutwfc,
            "ecutrho": ecutwfc * 10,
            "occupations": "smearing",
            "smearing": "marzari-vanderbilt",
            "degauss": 0.1 * (eV / Ry),
            "nosym": False,
            "noinv": False,
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
            "mixing_mode": "local-TF",
            "diagonalization": "cg",
        },
    }

    return Espresso(
        input_data=input_data,
        pseudopotentials=pseudopotentials,
        kpts=kpts,
        label=label,
    )


for i in [1200]:
    bulk = read("Cu-" + str(i) + "-3.61.pwo", index=-1)
    ads = read("espresso.pwo", index=-1)

    supercell_number = 3
    layer_number = 4
    slab_structure = fcc111(
        "Cu",
        (supercell_number, supercell_number, layer_number),
        a=bulk.cell.lengths()[0],
        vacuum=7.5,
        orthogonal=False,
        periodic=True,
    )
    slab_structure.translate([0, 0, -slab_structure.cell.cellpar()[2] * 0.65])
    constrain_bottom_layer = FixAtoms(indices=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    slab_structure.set_constraint(constrain_bottom_layer)
    add_adsorbate(slab_structure, ads, 1.95, "hcp", offset=1, mol_index=1)
    structure_trajectory = Trajectory("initial-structure.traj", "w")
    structure_trajectory.write(slab_structure)

    ecutwfc = i * (eV / Ry)
    user_prefix = "Cu"

    calc = ase_calc(
        label=user_prefix + "-" + str(i) + "-" + str(slab_structure.cell.cellpar()[0]),
        ecutwfc=ecutwfc,
    )
    slab_structure.calc = calc
    potentialenergy = slab_structure.get_potential_energy()
