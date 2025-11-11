FIDS=($(cat /store/carroll/repos/neon-isofit/deploy/crbu_2018_fids_failed_20251001.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=all_flightlines_1c_rerun_20251006_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=highcpu \
        --time=24:00:00 \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/neon-isofit/apply_oe/all_flightlines_1c_20251001.py --fid ${fid}"
done