FIDS=($(cat /store/carroll/repos/chess-isofit/2025/3c/1_deploy/ALMO_2025_fids.txt))
for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=shade_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/3c/3_shade/calculate_shade.py --fid ${fid} --solar_azimuth_band 4 --solar_zenith_band 5 --output_folder /store/carroll/col/data/2025/shade"
done

FIDS=($(cat /store/carroll/repos/chess-isofit/2025/3c/1_deploy/CRBU_2025_fids.txt))
for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=shade_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/3c/3_shade/calculate_shade.py --fid ${fid} --solar_azimuth_band 4 --solar_zenith_band 5 --output_folder /store/carroll/col/data/2025/shade"
done

FIDS=($(cat /store/carroll/repos/chess-isofit/2025/3c/1_deploy/UPTA_2025_fids.txt))
for fid in "${FIDS[@]}"; do
    sbatch \
        --job-name=shade_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/chess-isofit/2018/3c/3_shade/calculate_shade.py --fid ${fid} --solar_azimuth_band 4 --solar_zenith_band 5 --output_folder /store/carroll/col/data/2025/shade"
done