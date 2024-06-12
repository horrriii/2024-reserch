import json
import numpy as np

from ase import io
from ase.calculators.espresso import Espresso
from ase.units import *
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter


def ase_calc(label, ecutwfc):
    kpts = (1, 1, 1)

    pseudopotentials = json.load(open("./pslibrary.json"))

    input_data = {
        "control": {
            "calculation": "scf",
            "title": label,
            "outdir": "tmp",
            "prefix": label,
            "etot_conv_thr": 1e-5 * (eV / Ry),
            "forc_conv_thr": 0.01 * (eV / Ang) / (Ry / Bohr),
            "tprnfor": False,
            "tstress": False,
            "pseudo_dir": "/home/k0227/k022716/QE/pseudo/beef/",
        },
        "system": {
            "ecutwfc": ecutwfc,
            "ecutrho": ecutwfc * 10,
            "occupations": "from_input",
            "!one_atom_occupations": True,
            "nosym": False,
            "noinv": False,
            "nbnd": 12,
            "input_dft": "beef-vdw",
            "occupations": "from_input",
            "nspin": 2,
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

    additional_cards = []
    additional_cards.append("OCCUPATIONS")
    additional_cards.append(
        " ".join(map(str, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    )
    additional_cards.append(
        " ".join(map(str, [1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    )

    return Espresso(
        input_data=input_data,
        pseudopotentials=pseudopotentials,
        additional_cards=additional_cards,
        kpts=kpts,
        label=label,
    )


for i in [650, 750, 850, 950, 1050, 1200]:
    ecutwfc = i * (eV / Ry)

    atoms = io.read("cu.in", format="espresso-in")

    calc = ase_calc(label="espresso_" + str(i), ecutwfc=ecutwfc)
    atoms.set_initial_magnetic_moments([2.5 / 0.45454545454545453] * len(atoms))
    atoms.calc = calc
    atoms.get_potential_energy()
