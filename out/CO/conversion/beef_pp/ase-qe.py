import json

from ase.io import read, write
from ase.calculators.espresso import Espresso
from ase.units import *
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter

for i in [650,750,850,950,1050,1200]:
    ecutwfc=i*(eV/Ry)
    kpt_mesh=[1,1,1]

    co=read('CO.in',format='espresso-in')

    images_to_compute=[co]

    input_parameters=json.load(open('./input_parameters.json'))
    pseudos=json.load(open('./pslibrary.json'))
    user_prefix='Co'

    for image in images_to_compute:
        #traj_to_write_on = Trajectory(user_prefix+'-latcon'+'.traj','w')
        #image[0].magmom=(random.randint(0,200000)/100000)
        prefix='espresso'+str(i)
        input_parameters['control']['calculation']='relax'
        input_parameters['system']['input_dft']='beef-vdw'
        input_parameters['system']['ecutwfc']=ecutwfc
        input_parameters['system']['ecutrho']=ecutwfc*10
        #input_parameters['system']['degauss']=0.1*(eV/Ry)
        #input_parameters['system']['smearing']='marzari-vanderbilt'
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
        co.calc=calc
        etot=co.get_potential_energy()
        print('Total energy: %12.8f eV' % etot)
