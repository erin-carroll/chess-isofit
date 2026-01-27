sbatch \
    --job-name=mosaic_2018_shade_obs \
    --nodes=1 \
    --cpus-per-task=64 \
    --partition=standard \
    --mem=0 \
    --output=/home/carroll/logs/%j_%x.out \
    --error=/home/carroll/logs/%j_%x.err \
    --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/5_mosaic/3_mosaic_2018.py"

