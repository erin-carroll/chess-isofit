FIDS=($(cat /store/carroll/repos/chess-isofit/2018/3c/1_deploy/test_fids.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=test_3c_20251128_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --time=24:00:00 \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/3c/1_deploy/7_test_rccs_pressureelev_20251128.py --fid ${fid}"
done