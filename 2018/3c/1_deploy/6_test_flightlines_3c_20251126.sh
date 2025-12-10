FIDS=($(cat /store/carroll/repos/chess-isofit/2018/3c/1_deploy/crbu_2018_fids_test.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=test_3c_20251126_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/3c/1_deploy/5_weird_flightlines_test_20251126.py --fid ${fid}"
done