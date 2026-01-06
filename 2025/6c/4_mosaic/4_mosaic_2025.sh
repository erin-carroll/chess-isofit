DOMAINS=($(cat /store/carroll/repos/chess-isofit/2025/data_prep/domains.txt))

for domain in "${DOMAINS[@]}"; do
    sbatch \
        --job-name=mosaic_2025_shade_${domain} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=standard \
        --mem=0 \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2025/6c/4_mosaic/4_mosaic_2025.py --domain ${domain}"
done