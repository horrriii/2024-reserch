import json

from ase.io import read, write
from ase import Atoms
from ase.calculators.espresso import Espresso
from ase.units import * # type: ignore
from ase.build import bulk, fcc111, add_adsorbate
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter
from ase.constraints import FixAtoms


def ase_calc(label, ecutwfc, outdir):
    kpts = (8, 8, 1)

    pseudopotentials = json.load(open("./../../../pslibrary.json"))

    input_data = {
        "control": {
            "calculation": "relax",
            "restart_mode": "restart",
            "wf_collect" : True,
            "nstep" : 100,
            "title": label,
            "verbosity": "high",
            "outdir": outdir,
            "prefix": label,
            "etot_conv_thr": 1e-5 * (eV / Ry),
            "forc_conv_thr": 0.01 * (eV / Ang) / (Ry / Bohr),
            "tprnfor": True,
            "tstress": False,
            "disk_io" : "nowf",
            "max_seconds":86000,
            "pseudo_dir": "/home/k0227/k022716/QE/pseudo/",
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
            "mixing_mode": "local-TF",
            "diagonalization": "cg",
            "diago_david_ndim": 2,
        },
    }

    return Espresso(
        input_data=input_data,
        pseudopotentials=pseudopotentials,
        kpts=kpts,
        label=label,
    )

for i in [850]:
    ecutwfc = i * (eV / Ry)
    bulk=read('espresso_'+str(i)+'.pwo', index=-1)
    co=Atoms('CO',[(0, 0, 0), (0, 0, 1.13)])
    
    supercell_number=3
    layer_number=4
    slab_structure=fcc111('Cu',(supercell_number,supercell_number,layer_number),a=bulk.cell.lengths()[0],vacuum=7.5,orthogonal=False,periodic=True) # type: ignore
    slab_structure.translate([0,0,-slab_structure.cell.cellpar()[2]*0.65])
    constrain_bottom_layer=FixAtoms(indices=[0,1,2,3,4,5,6,7,8])
    slab_structure.set_constraint(constrain_bottom_layer)
    add_adsorbate(slab_structure,co,1.95,'ontop',offset=1,mol_index=1)
    print('Made images for 111 surface!')
    
    
    calc = ase_calc(label="slab_"+str(i), ecutwfc=ecutwfc, outdir='tmp_'+str(i))
    slab_structure.calc = calc
    slab_structure.get_potential_energy()
