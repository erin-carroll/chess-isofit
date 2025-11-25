FIDS=($(cat /store/carroll/repos/chess-isofit/2025/3c/2_validation/insitu_validation_2025_fids.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=applyoe_rcc_validation_2025_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=highcpu \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2025/3c/2_validation/2_applyoe_rcc_validation.py --fid ${fid}"
done