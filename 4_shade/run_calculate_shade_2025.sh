FID_FILES=(
  /store/carroll/col/data/2025/mosaic/file_lists/ALMO_2025_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/CRBU_2025_fids.txt
  /store/carroll/col/data/2025/mosaic/file_lists/UPTA_2025_fids.txt
)

for f in "${FID_FILES[@]}"; do
  while IFS= read -r fid; do
    [[ -z "$fid" ]] && continue
    sbatch \
      --job-name="shade_${fid}" \
      --nodes=1 \
      --cpus-per-task=64 \
      --partition=patient \
      --mem=300G \
      --output=/home/carroll/logs/%j_%x.out \
      --error=/home/carroll/logs/%j_%x.err \
      --wrap="python /store/carroll/repos/chess-isofit/4_shade/calculate_shade.py --fid ${fid} --solar_azimuth_band 4 --solar_zenith_band 5 --output_folder /store/carroll/col/data/2025/shade"
  done < "$f"
done