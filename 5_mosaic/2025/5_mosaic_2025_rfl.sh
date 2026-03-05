DOMAINS=(ALMO CRBU UPTA)

for domain in "${DOMAINS[@]}"; do
    sbatch \
        --job-name=mosaic_rfl_${domain}_2025 \
        --nodes=1 \
        --cpus-per-task=1 \
        --partition=standard \
        --mem=200G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="python /store/carroll/repos/chess-isofit/5_mosaic/2025/5_mosaic_2025_rfl.py --domain ${domain}"
done