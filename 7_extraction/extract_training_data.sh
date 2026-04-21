FID_FILES=(
  /store/carroll/col/data/2018/mosaic/file_lists/CRBU_2018_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/ALMO_2025_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/CRBU_2025_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/UPTA_2025_fids.txt
)

for f in "${FID_FILES[@]}"; do
  while IFS= read -r fid; do
    [[ -z "$fid" ]] && continue
    sbatch \
        --job-name=extract_${fid} \
        --nodes=1 \
        --cpus-per-task=8 \
        --partition=standard \
        --mem=100G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/7_extraction/extract_training_data.py --fid ${fid}"
  done < "$f"
done