import os
import json
import math
import random

from ase.io import read, write
from ase.calculators.espresso import Espresso
from ase.units import *
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter
from ase.build import fcc111, bulk
from ase.io.trajectory import Trajectory
from ase.constraints import FixAtoms

a=3.61
n_processors=76

bulk_structure=bulk('Cu', 'fcc', a , cubic=True)

for i in [1200]:
    ecutwfc=i*(eV/Ry)
    kpt_mesh=[24,24,24]

    images_to_compute=[bulk_structure]

    input_parameters=json.load(open('./input_parameters.json'))
    pseudos=json.load(open('./pslibrary.json'))
    user_prefix='Cu'

    for image in images_to_compute:
        prefix=user_prefix+'-'+str(i)+'-'+str(image.cell.cellpar()[0])
        input_parameters['control']['calculation']='vc-relax'
        input_parameters['system']['input_dft']='beef-vdw'
        input_parameters['system']['ecutwfc']=ecutwfc
        input_parameters['system']['ecutrho']=ecutwfc*10
        input_parameters['system']['degauss']=0.1*(eV/Ry)
        input_parameters['system']['smearing']='marzari-vanderbilt'
        input_parameters['system']['nosym']=False
        input_parameters['system']['noinv']=False
        input_parameters['control']['title']=prefix
        input_parameters['control']['nstep']=100
        input_parameters['control']['prefix']=prefix
        input_parameters['control']['etot_conv_thr']= 1e-5*(eV/Ry)
        input_parameters['control']['forc_conv_thr']= 0.01*(eV/Ang)/(Ry/Bohr)
        input_parameters['control']['restart_mode']='from_scratch'
        input_parameters['electrons']['conv_thr']=1e-10*(eV/Ry)
        input_parameters['electrons']['mixing_beta']=1/3
        input_parameters['ions']['ion_dynamics']='bfgs'
        write(prefix+'.pwi',image,'espresso-in',kpts=kpt_mesh,crystal_coordinates=False,input_data=input_parameters,pseudopotentials=pseudos,tstress=False,tprnfor=True)
        calc = Espresso(label=prefix, pseudopotentials=pseudos,input_data=input_parameters, tstress=False, tprnfor=True, kpts=kpt_mesh)
        bulk_structure.calc=calc
        write('cu_fcc.xyz',bulk_structure)
        etot=bulk_structure.get_potential_energy()
        print('Total energy: %12.8f eV' % etot)
