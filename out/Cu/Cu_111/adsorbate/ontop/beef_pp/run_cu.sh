#!/bin/sh
#SBATCH --partition=F16cpu
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=128
#SBATCH --time=24:00:00
#SBATCH --job-name=Cu_ads

export FI_PROVIDER=psm3
ulimit -s unlimited
#
module purge
module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0
#
export ASE_ESPRESSO_COMMAND="mpirun ${HOME}/QE/src/qe-7.2/bin/pw.x -in PREFIX.pwi > PREFIX.pwo"
export ESPRESSO_PSEUDO="/home/k0227/k022716/QE/pseudo"

echo "========= Job started  at `date` =========="

python3 slab_ads.py

echo "========= Job finished at `date` =========="
