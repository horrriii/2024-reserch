import json

from ase.io import read, write
from ase import Atoms
from ase.calculators.espresso import Espresso
from ase.units import * # type: ignore
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter


def ase_calc(label, ecutwfc):
    kpts = (1, 1, 1)

    pseudopotentials = json.load(open("./../pslibrary.json"))

    input_data = {
        "control": {
            "calculation": "relax",
            "restart_mode": "restart",
            "title": label,
            "verbosity": "high",
            "outdir": "tmp",
            "prefix": label,
            "etot_conv_thr": 1e-5 * (eV / Ry),
            "forc_conv_thr": 0.01 * (eV / Ang) / (Ry / Bohr),
            "tprnfor": True,
            "tstress": False,
            # "pseudo": "/home/r0147/r014705/QE/pseudo/",
        },
        "system": {
            "ecutwfc": ecutwfc,
            "ecutrho": ecutwfc * 10,
            # "occupations": "smearing",
            # "smearing": "marzari-vanderbilt",
            # "degauss": 0.1 * (eV / Ry),
            "nosym": True,
            "noinv": True,
            "input_dft": "beef-vdw",
            # "assume_isolated": "esm",
            # "esm_bc": "bc3",
            # "esm_w": 0,
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


for i in [1050,1200]:
    ecutwfc = i * (eV / Ry)
    co = Atoms("CO", [(0, 0, 0), (0, 0, 1.13)], cell=(15, 15, 15), pbc=True)
    
    calc = ase_calc(label="espresso_"+str(i), ecutwfc=ecutwfc)
    co.calc = calc
    co.get_potential_energy()
