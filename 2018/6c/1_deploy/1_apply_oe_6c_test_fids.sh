FIDS=($(cat /store/carroll/repos/chess-isofit/2018/6c/1_deploy/crbu_2018_fids_test.txt))

for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=test_6c_2018_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=highcpu \
        --mem=375G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/6c/1_deploy/0_apply_oe_6c.py --fid ${fid}"
done