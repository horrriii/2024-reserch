#!/bin/sh
#SBATCH -J h2o
#SBATCH -p F4cpu
#SBATCH -N 2
#SBATCH -n 128
#SBATCH -c 2
#SBATCH -o LOG
#SBATCH -e err

#
echo started at 'date'
#
module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0
#
INPUT_FILE='relax.in'
OUTPUT_FILE='relax.out'
#
PW_DIR=${HOME}/QE/src/qe-7.2/bin
PW_COMMAND=pw.x
PW=$PW_DIR/$PW_COMMAND
#
srun ${PW} < ${INPUT_FILE} > ${OUTPUT_FILE}
#
ls -lrt
echo finifhed at 'date'
