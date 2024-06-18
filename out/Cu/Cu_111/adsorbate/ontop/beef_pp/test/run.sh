#!/bin/sh
#SBATCH --partition=F4cpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=24:00:00
#SBATCH --job-name=calc
#SBATCH --array=0-59

# -- ENVIRONMENT --------------------------------------------------------------
source ~/.bashrc
# module purge
# module load oneapi_compiler/2023.0.0 oneapi_mkl/2023.0.0 oneapi_mpi/2023.0.0
module list

export FI_PROVIDER=psm3
ulimit -s unlimited

# Activate QE environment ------------------------------------------------------
export PATH=$HOME/QE/src/qe-7.2/bin:$PATH
export ESPRESSO_PSEUDO=$HOME/QE/pseudo/gbrv
# export ESPRESSO_TMPDIR=TMPDIR
export ESPRESSO_TMPDIR="/work/k0227/k022715"/TMPDIR_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}

export ASE_ESPRESSO_COMMAND='srun pw.x -nk 2 pw.x -in PREFIX.pwi > PREFIX.pwo'

# Activate Python environment --------------------------------
mamba activate qe
echo "CONDA ENV: " $CONDA_PREFIX


# -- EXECUTION ----------------------------------------------------------------
echo "========= Job started  at `date` =========="

python 01_run_scan.py

echo "========= Job finished at `date` =========="

