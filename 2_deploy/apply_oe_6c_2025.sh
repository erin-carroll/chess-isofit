FID_FILES=(
  /store/carroll/col/data/2025/mosaic/file_lists/ALMO_2025_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/CRBU_2025_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/UPTA_2025_fids.txt
)

for f in "${FID_FILES[@]}"; do
  while IFS= read -r fid; do
    [[ -z "$fid" ]] && continue
    sbatch \
        --job-name=deploy_6c_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=highcpu \
        --mem=375G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2_deploy/apply_oe_6c.py --fid ${fid}"
  done < "$f"
done
