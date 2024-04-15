#!/bin/bash
#PBS -q DBG
#PBS --group=k0227
#PBS -m b
#PBS -T intmpi
#PBS -l cpunum_job=64
#PBS -v OMP_NUM_THREADS=2
#PBS -l elapstim_req=00:10:00
#PBS -e ERR
#PBS -o OUT

module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0

INPUT_FILE='relax.in'
OUTPUT_FILE='relax.out'
#
PW_DIR=${HOME}/QE/src/qe-7.2/bin
#
MPI_COMMAND="mpirun ${NQSV_MPIOPTS}"
PW_COMMAND=pw.x
PW=$PW_DIR/$PW_COMMAND
#
cd ${PBS_O_WORKDIR}
#
${MPI_COMMAND} ${PW} < ${INPUT_FILE} > ${OUTPUT_FILE}

