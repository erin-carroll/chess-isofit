sbatch \
    --job-name=mosaic_2018_rgb \
    --nodes=1 \
    --cpus-per-task=64 \
    --partition=standard \
    --mem=0 \
    --output=/home/carroll/logs/%j_%x.out \
    --error=/home/carroll/logs/%j_%x.err \
    --wrap="python /store/carroll/repos/chess-isofit/5_mosaic/2018/3_mosaic_2018.py"

