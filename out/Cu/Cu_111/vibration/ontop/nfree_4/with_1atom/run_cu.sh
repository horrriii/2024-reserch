#!/bin/sh
#SBATCH -J Cu_111
#SBATCH -p F16cpu
#SBATCH -N 6

export FI_PROVIDER=psm3
ulimit -s unlimited
#
module purge
module load oneapi_compiler/2023.0.0
module load oneapi_mkl/2023.0.0
module load oneapi_mpi/2023.0.0
#
#export ASE_ESPRESSO_COMMAND="srun ${HOME}/QE/src/qe-7.2/bin/pw.x -nk 3 -nb 32 -ntg 4 -nd 1 -in PREFIX.pwi > PREFIX.pwo"
export ASE_ESPRESSO_COMMAND="srun -n 192 -c 4 -N 6 ${HOME}/QE/src/qe-7.2/bin/pw.x -in PREFIX.pwi | tee PREFIX.pwo"
export ESPRESSO_PSEUDO="/home/k0227/k022716/QE/pseudo"

# 監視するディレクトリパス
WATCH_DIR="/home/k0227/k022716/QE/out/Cu/Cu_111/vibration/ontop/nfree_4/with_1atom"
# バックアップ先のディレクトリパス
BACKUP_DIR="/home/k0227/k022716/QE/out/Cu/Cu_111/vibration/ontop/nfree_4/with_1atom/backup"

# .pwiファイルの変更を監視
inotifywait -m -e create,modify --format '%w%f' "${WATCH_DIR}" --exclude '.*[^pwi]$' | while read FILE
do
    # バックアップファイルのパスを作成（タイムスタンプ付き）
    TIMESTAMP=$(date +%Y%m%d%H%M%S)
    BASENAME=$(basename "${FILE}")
    BACKUP_FILE="${BACKUP_DIR}/${BASENAME}_${TIMESTAMP}"
    
    # ファイルをバックアップディレクトリにコピー
    cp "${FILE}" "${BACKUP_FILE}"
    echo "Backed up: ${FILE} -> ${BACKUP_FILE}"
done

echo "========= Job started  at `date` =========="

python3 vib_run.py | tee python.log

echo "========= Job finished at `date` =========="
