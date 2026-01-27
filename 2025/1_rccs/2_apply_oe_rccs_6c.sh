FIDS=($(cat /store/carroll/repos/chess-isofit/2025/6c/0_rccs/rcc_subsets_2025_fids.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=3025_rccs_6c_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=highcpu \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2025/6c/0_rccs/3_apply_oe_rccs_6c.py --fid ${fid}"
done

