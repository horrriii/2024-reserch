#!/bin/sh
#SBATCH -J Cu_ads
#SBATCH -p F4cpu
#SBATCH -N 2
#SBATCH -n 64
#SBATCH -c 2

export FI_PROVIDER=psm3
export OMP_NUM_THREADS=2
ulimit -s unlimited
#
module purge
module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0
#
export ASE_ESPRESSO_COMMAND="srun ${HOME}/QE/src/qe-7.2/bin/pw.x -in PREFIX.pwi > PREFIX.pwo"
export ESPRESSO_PSEUDO="/home/k0227/k022716/QE/pseudo"

echo "========= Job started  at `date` =========="

python3 slab_850.py | tee python.log

echo "========= Job finished at `date` =========="
