import os
import json
import re
import math
import subprocess
import random
import numpy as np


from random import randint
from ase import io

from ase.calculators.espresso import Espresso
from ase.optimize import BFGS, GPMin, BFGSLineSearch
from ase.data import atomic_numbers, atomic_names, atomic_masses, covalent_radii, chemical_symbols
from ase.units import *
from ase.calculators.socketio import SocketIOCalculator
from ase.vibrations import Vibrations
from ase.thermochemistry import HarmonicThermo
from ase.build import fcc111,bulk,molecule,add_adsorbate
from ase.io.trajectory import Trajectory
from ase.constraints import FixAtoms

job_id = os.environ['PBS_JOBID']
pwd = str(os.getcwd())
n_processors=76
exchange_correlation=str(os.path.basename(os.path.dirname(os.getcwd())))
#bulk=io.read('Ag-4.09.pwo',index=-1)
#supercell_number=3
#layer_number=4
slab_structure=io.read('relaxed.pwo',index=-1)
#slab_structure.translate([0,0,-slab_structure.cell.cellpar()[2]*0.65])
constrain_bottom_layer=FixAtoms(indices=[0,1,2,3,4,5,6,7,8])
slab_structure.set_constraint(constrain_bottom_layer)
#adsorbate_molecule=molecule('CO')
#add_adsorbate(slab_structure,adsorbate_molecule,1.95,'ontop',offset=1,mol_index=1)
print('Made images for 111 surface!')
structure_trajectory=Trajectory('initial-structure.traj','w')
structure_trajectory.write(slab_structure)

ecutwfc = 650*(eV/Ry)
kpt_mesh = [8, 8, 1]
port = 31415

nk=math.gcd(int(n_processors),2*(kpt_mesh[0]*kpt_mesh[1]*kpt_mesh[2]))
ntg = 1
nd = 1
nb = int(int(n_processors)/int(nk))

images_to_compute=[slab_structure]

input_parameters=json.load(open('./input_parameters.json'))
pseudos=json.load(open('./pslibrary.json'))
user_prefix='Ag-111'

for image in images_to_compute:
    traj_to_write_on = Trajectory(user_prefix+'-latcon'+'.traj','w')
    prefix=user_prefix+'-vib'
    input_parameters['control']['calculation']='scf'

    if str(os.path.basename(os.getcwd())) == 'rpbe+d2':
            exchange_correlation='rpbe'
            input_parameters['system']['vdw_corr']='grimme-d2'
    elif str(os.path.basename(os.getcwd())) == 'pbe+d2':
            exchange_correlation='pbe'
            input_parameters['system']['vdw_corr']='grimme-d2'
    else:
            pass

    input_parameters['system']['input_dft']=exchange_correlation
    input_parameters['system']['ecutwfc']=ecutwfc
    input_parameters['system']['ecutrho']=ecutwfc*10
    input_parameters['system']['degauss']=0.1*(eV/Ry)
    input_parameters['system']['smearing']='marzari-vanderbilt'
    input_parameters['system']['nosym']=True
    input_parameters['system']['noinv']=True
    input_parameters['system']['assume_isolated']='esm'
    input_parameters['system']['esm_bc']='bc3'
    input_parameters['system']['esm_w']=0
    input_parameters['control']['title']=prefix
    input_parameters['control']['disk_io']='nowf'
    input_parameters['control']['nstep']=100
    input_parameters['control']['prefix']=prefix
    input_parameters['control']['etot_conv_thr']= 1e-4*(eV/Ry)
    input_parameters['control']['restart_mode']='from_scratch'
    input_parameters['electrons']['conv_thr']=1e-10*(eV/Ry)
    input_parameters['electrons']['mixing_beta']=1/3
    io.write(prefix+'.pwi',image,'espresso-in',kpts=kpt_mesh,crystal_coordinates=False,input_data=input_parameters,pseudopotentials=pseudos,tstress=True,tprnfor=True)
    ase_command = 'mpirun -np 128' \
            +' ./pw.x' \
            +' -nk 32 -nb 4 -in'+' '+prefix+'.pwi' \
            +' | tee '+prefix+'.pw.out' \
            +' | tee '+prefix+'.pwo' \
            +' | tee -a '+user_prefix+'.continuous.LOG'
    os.environ['ASE_ESPRESSO_COMMAND'] = ase_command
    print('ASE_ESPRESSO_COMMAND is '+'"'+ase_command+'"')
    espresso = Espresso(label=prefix, input_data=input_parameters, pseudopotentials=pseudos, kpts=kpt_mesh,tstress=True,tprnfor=True)
    image.calc=espresso
    image_potential_energy=image.get_potential_energy()
    print('E_DFT with a='+str(image.cell.cellpar()[0])+'='+str(image_potential_energy))
    traj_to_write_on.write(image)
    vib=Vibrations(image,indices=[-2,-1],nfree=4)
    vib.run()
    vib.summary(log='vibrational-frequencies.txt')
    vib.write_mode()
    vib_energies=vib.get_energies()
    vib_frequencies=vib.get_frequencies()
    thermo=HarmonicThermo(vib_energies=vib_energies,potentialenergy=image_potential_energy)
    T_ambient=298.15
    U=thermo.get_internal_energy(temperature=T_ambient)
    S=thermo.get_entropy(temperature=T_ambient)
    A=thermo.get_helmholtz_energy(temperature=T_ambient)
    with open('helmholtz','w') as helmholtz_file:
           helmholtz_file.write(str(A))
