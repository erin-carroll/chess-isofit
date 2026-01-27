FIDS=($(cat /store/carroll/repos/chess-isofit/2025/3c/2_validation/mineral_exposure/mineral_exposure_fids.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=mineral_exposed_6c_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=standard \
        --time=24:00:00 \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2025/3c/2_validation/mineral_exposure/mineral_exposure_6c.py --fid ${fid}"
done