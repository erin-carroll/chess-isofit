all_obs_files="/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt"
mosaic_glt_out="/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt_analytical.tif"
log_file="/home/carroll/logs/mosaic_2018_analytical.log"
sbatch \
    --job-name="mosaic_2018_analytical" \
    --nodes=1 \
    --cpus-per-task=64 \
    --partition=standard \
    --mem=0 \
    --output=/home/carroll/logs/%j_%x.out \
    --error=/home/carroll/logs/%j_%x.err \
    --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc-analytical ${mosaic_glt_out} ${all_obs_files} --x_resolution 1 --output_epsg 32613 --log_file ${log_file} --criteria_band 5 --criteria_mode min"