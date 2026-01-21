ul_lr_list="/store/carroll/col/data/2018/mosaic/file_lists/ul_lr_grids_cloudshadow_rerun.txt"
all_obs_files="/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt"

while read -r line; do
    clean=$(echo "$line" | tr -d '[],')
    read -r ulx uly lrx lry <<< "$clean"
    id="${ulx}_${uly}_${lrx}_${lry}"

    mosaic_glt_out="/store/carroll/col/data/2018/mosaic/CRBU_2018_mosaic_glt_cloudshadow_${id}.tif"
    log_file="/home/carroll/logs/mosaic_glt_CRBU_2018_cloudshadow_${id}.log"
    deprioritize_file_list="/store/carroll/col/data/2018/mosaic/file_lists/deprioritize_obs_2018.txt"
    cloud_shadow_mask_list="/store/carroll/col/data/2018/mosaic/file_lists/cloud_shadow_CRBU_2018.txt"
    sbatch \
        --job-name="mosaic_2018_CRBU_${id}" \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=standard \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="export MKL_NUM_THREADS=1; export OMP_NUM_THREADS=1; python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc-cloudshadow ${mosaic_glt_out} ${all_obs_files} --deprioritize_file_list ${deprioritize_file_list} --cloud_shadow_mask_list ${cloud_shadow_mask_list} --x_resolution 1 --output_epsg 32613 --target_extent_ul_lr ${ulx} ${uly} ${lrx} ${lry} --log_file ${log_file} --log_level DEBUG --n_cores 64 --criteria_band 5 --criteria_mode min"

done < "$ul_lr_list"
