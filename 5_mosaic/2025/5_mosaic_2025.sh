DOMAINS=(CRBU)

for domain in "${DOMAINS[@]}"; do
    sbatch \
        --job-name=mosaic_2025_${domain} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=standard \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="python /store/carroll/repos/chess-isofit/5_mosaic/2025/5_mosaic_2025.py --domain ${domain}"
done