domain="UPTA"
year="2018"

ul_lr_list="/store/carroll/col/data/2025/mosaic/file_lists/ul_lr_grids_${domain}.txt"
all_obs_files="/store/carroll/col/data/${year}/mosaic/file_lists/top_priority_obs_${domain}.txt"

while read -r line; do
    clean=$(echo "$line" | tr -d '[],')
    read -r ulx uly lrx lry <<< "$clean"
    id="${ulx}_${lry}"

    mosaic_glt_out="/store/carroll/col/data/${year}/mosaic/glt_tiled/${domain}/${domain}_${year}_mosaic_glt_${id}.tif"
    if [[ -f "$mosaic_glt_out" ]]; then
        echo "Skipping existing: $mosaic_glt_out"
        continue
    fi

    log_file="/home/carroll/logs/mosaic_glt_${domain}_${year}_${id}.log"
    deprioritize_file_list="/store/carroll/col/data/${year}/mosaic/file_lists/deprioritize_obs.txt"
    cloud_shadow_mask_list="/store/carroll/col/data/${year}/mosaic/file_lists/cloud_shadow_${domain}.txt"
    sbatch \
        --job-name="glt_${domain}_${id}" \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=standard \
        --mem=175G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc-cloudshadow ${mosaic_glt_out} ${all_obs_files} --deprioritize_file_list ${deprioritize_file_list} --cloud_shadow_mask_list ${cloud_shadow_mask_list} --x_resolution 1 --output_epsg 32613 --target_extent_ul_lr ${ulx} ${uly} ${lrx} ${lry} --log_file ${log_file} --log_level DEBUG --n_cores 64 --criteria_band 5 --criteria_mode min"

done < "$ul_lr_list"
