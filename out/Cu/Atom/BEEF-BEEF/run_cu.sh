#!/bin/sh
#SBATCH -J Cu_atom
#SBATCH -p i8cpu
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -c 4
#SBATCH -t 00:30:00

export FI_PROVIDER=psm3
ulimit -s unlimited

module purge
module load oneapi_compiler/2023.0.0 oneapi_mkl/2023.0.0 oneapi_mpi/2023.0.0

export ASE_ESPRESSO_COMMAND="srun ${HOME}/QE/src/qe-7.2/bin/pw.x -in PREFIX.pwi > PREFIX.pwo"
export ESPRESSO_PSEUDO="/home/k0227/k022716/QE/pseudo"

python3 ase-qe_new.py
