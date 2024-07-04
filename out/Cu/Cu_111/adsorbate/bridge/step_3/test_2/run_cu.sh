#!/bin/sh
#SBATCH -J Cu_111
#SBATCH -p F16cpu
#SBATCH -N 6

export FI_PROVIDER=psm3
export OMP_NUM_THREADS=2
ulimit -s unlimited
#
module purge
module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0
#
#export ASE_ESPRESSO_COMMAND="srun ${HOME}/QE/src/qe-7.2/bin/pw.x -nk 3 -nb 32 -ntg 4 -nd 1 -in PREFIX.pwi > PREFIX.pwo"
export ASE_ESPRESSO_COMMAND="srun --exclusive --mem-per-cpu=1840 -n 192 -c 4 -N 6 ${HOME}/QE/src/qe-7.2/bin/pw.x -nk 3 -nb 16 -ntg 4 -nd 1 -in PREFIX.pwi | tee PREFIX.pwo"
export ESPRESSO_PSEUDO="/home/k0227/k022716/QE/pseudo"


echo "========= Job started  at `date` =========="

python3 slab_ads.py | tee python.log

echo "========= Job finished at `date` =========="
