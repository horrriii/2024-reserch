#!/bin/sh
#SBATCH -J Cu_atom
#SBATCH -p i8cpu
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -c 1
#SBATCH -o LOG
#SBATCH -e ERR

#
echo started at 'date'
#
module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0
#
export ASE_ESPRESSO_COMMAND="mpirun ${HOME}/QE/src/qe-7.2/bin/pw.x -in PREFIX.pwi > PREFIX.pwo"
export ESPRESSO_PSEUDO="/home/k0227/k022716/QE/pseudo"
 
python3 ase-qe.py
