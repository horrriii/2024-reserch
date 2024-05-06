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

n_processors=76

bulk=read('espresso.pwo', index=-1)

supercell_number=3
layer_number=4
slab_structure=fcc111('Cu',(supercell_number,supercell_number,layer_number),a=bulk.cell.lengths()[0],vacuum=7.5,orthogonal=False,periodic=True)
slab_structure.translate([0,0,-slab_structure.cell.cellpar()[2]*0.65])
constrain_bottom_layer=FixAtoms(indices=[0,1,2,3,4,5,6,7,8])
slab_structure.set_constraint(constrain_bottom_layer)
#adsorbate_molecule=molecule('CO')
#add_adsorbate(slab_structure,adsorbate_molecule,1.95,'ontop',offset=1,mol_index=1)
print('Made images for 111 surface!')
structure_trajectory=Trajectory('initial-structure.traj','w')
structure_trajectory.write(slab_structure)





ecutwfc=650*(eV/Ry)
kpt_mesh=[8,8,1]
port=31415

nk=math.gcd(int(n_processors),2*(kpt_mesh[0]*kpt_mesh[1]*kpt_mesh[2]))
ntg = 1
nd = 1
nb = int(int(n_processors)/int(nk))

images_to_compute=[slab_structure]

input_parameters=json.load(open('./../input_parameters.json'))
pseudos=json.load(open('./../pslibrary.json'))
user_prefix='Cu-111'

for image in images_to_compute:
    traj_to_write_on = Trajectory(user_prefix+'-latcon'+'.traj','w')
    image[0].magmom=(random.randint(0,200000)/100000)
    prefix=user_prefix+'-'+str(image.cell.cellpar()[0])
    input_parameters['control']['calculation']='relax'
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
    input_parameters['control']['restart_mode']='from_scratch'
    input_parameters['electrons']['conv_thr']=1e-10*(eV/Ry)
    input_parameters['electrons']['mixing_beta']=1/3
    input_parameters['ions']['ion_dynamics']='bfgs'
    write(prefix+'.pwi',image,'espresso-in',kpts=kpt_mesh,crystal_coordinates=False,input_data=input_parameters,pseudopotentials=pseudos,tstress=True,tprnfor=True)
    espresso = Espresso(label=prefix, input_data=input_parameters, pseudopotentials=pseudos, kpts=kpt_mesh,tstress=True,tprnfor=True)
    image.calc=espresso
    image_potential_energy=image.get_potential_energy()
