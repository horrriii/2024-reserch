#!/bin/sh
#SBATCH -J Atom
#SBATCH -p i8cpu
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -c 4
#SBATCH -t 00:30:00
#
module purge
module load oneapi_compiler/2023.0.0 oneapi_mkl/2023.0.0 oneapi_mpi/2023.0.0
#
JOB_LIST='scf'
#
PREFIX='cu'
#
SEEDNAME=''
#
# Parallelization level
#
NPOOLS=2
NBAND=1
#
# MPI command
#
MPI_COMMAND=srun
#
# PW commands
#
PW_DIR="${HOME}/QE/src/qe-7.2/bin"
PSEUDO_DIR="${HOME}/QE/pseudo"
PW="${PW_DIR}/pw.x -npools ${NPOOLS} -nband ${NBAND}"
PH="${PW_DIR}/ph.x -npools ${NPOOLS} -nband ${NBAND}"
MATDYN="${PW_DIR}/matdyn.x -npools ${NPOOLS} -nband ${NBAND}"
PROJWFC="${PW_DIR}/projwfc.x -npools ${NPOOLS} -nband ${NBAND}"
PW2WAN="${PW_DIR}/pw2wannier90.x -npools ${NPOOLS} -nband ${NBAND}"
HP="${PW_DIR}/hp.x -npools ${NPOOLS} -nband ${NBAND}"
W90="${PW_DIR}/wannier90.x"
THPW="${PW_DIR}/thermo_pw.x -ni ${NIMAGE}"
#
for JOB in ${JOB_LIST}
do
if [ -z ${PREFIX} ];
then
INPUT_FILE=${JOB}'.in'
OUTPUT_FILE=${JOB}'.out'
else
INPUT_FILE=${PREFIX}'_'${JOB}'.in'
OUTPUT_FILE=${PREFIX}'_'${JOB}'.out'
if [ ! -e ${INPUT_FILE} ];
then
INPUT_FILE=${PREFIX}'.'${JOB}'.in'
OUTPUT_FILE=${PREFIX}'.'${JOB}'.out'
fi
fi
#
ulimit -s unlimited
#
if [ ${JOB} == 'scf' ];
then
${MPI_COMMAND} ${PW} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'nscf' ];
then
${MPI_COMMAND} ${PW} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'relax' ];
then
${MPI_COMMAND} ${PW} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'vc-relax' ];
then
${MPI_COMMAND} ${PW} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'ph' ];
then
${MPI_COMMAND} ${PH} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'phG' ];
then
${MPI_COMMAND} ${PH} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'hp' ];
then
${MPI_COMMAND} ${HP} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'matdyn' ];
then
${MPI_COMMAND} ${MATDYN} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'projwfc' ];
then
${MPI_COMMAND} ${PROJWFC} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'pw2wan' ];
then
${MPI_COMMAND} ${PW2WAN} < ${INPUT_FILE} > ${OUTPUT_FILE}
elif [ ${JOB} == 'w90pp' ];
then
${MPI_COMMAND} ${W90} -pp ${SEEDNAME}
elif [ ${JOB} == 'w90' ];
then
${MPI_COMMAND} ${W90} ${SEEDNAME}
elif [ ${JOB} == 'thpw' ];
then
${MPI_COMMAND} ${THPW} < ${INPUT_FILE} > ${OUTPUT_FILE}
fi
done
