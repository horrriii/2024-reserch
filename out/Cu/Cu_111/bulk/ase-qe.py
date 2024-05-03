import json

from ase.io import read, write
from ase.calculators.espresso import Espresso
from ase.units import *
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter

ecutwfc=650*(eV/Ry)
kpt_mesh=[8,8,8]

pseudos=json.load(open('./../pslibrary.json'))

qe_input_data = {'control': {'calculation' : 'vc-relax',
                             'outdir' : './tmp/',
                             'prefix' : 'Cu_111',
                             'nstep'  : 100,
                             'etot_conv_thr' : 1e-5*(eV/Ry),
                             'restart_mode' : 'from_scratch'
                            },
                 'system':  {'ecutwfc': ecutwfc,
                             'ecutrho': ecutwfc*10,
                             'occupations' : 'smearing',
                             'smearing' : 'marzari-vanderbilt',
                             'degauss' : 0.1*(eV/Ry),
                             'input_dft' : 'BEEF-vdW'
                            },
                 'electrons': {'diagonalization' : 'david',
                               'conv_thr'        : 1.0e-10*(eV/Ry),
                               'mixing_beta'     : 1/3
                              },
                 'ions': {'ion_dynamics' : 'bfgs'
                         }
                 }
pseudopotentials = pseudos
calc = Espresso(pseudopotentials=pseudopotentials,input_data=qe_input_data,
                tstress=True, tprnfor=True, kpts=kpt_mesh)
cu=read('Cu_fcc.in',format='espresso-in')
cu.calc = calc
write('cu_opt.xyz',cu)
etot=cu.get_potential_energy()
print('Total energy: %12.8f eV' % etot)
