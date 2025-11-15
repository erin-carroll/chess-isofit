ul_lr_list="/store/carroll/col/data/2018/mosaic/file_lists/ul_lr_grids.txt"
all_obs_files="/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt"

while read -r line; do
    clean=$(echo "$line" | tr -d '[],')
    read -r ulx uly lrx lry <<< "$clean"
    id="${ulx}_${uly}_${lrx}_${lry}"

    mosaic_glt_out="/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt_${id}.tif"
    log_file="/home/carroll/logs/mosaic_glt_${id}.log"

    sbatch \
        --job-name="mosaic_2018_${id}" \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc ${mosaic_glt_out} ${all_obs_files} --x_resolution 1 --output_epsg 32613 --target_extent_ul_lr ${ulx} ${uly} ${lrx} ${lry} --log_file ${log_file} --n_cores 64 --criteria_band 5 --criteria_mode min"

done < "$ul_lr_list"
