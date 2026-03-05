DOMAINS=(ALMO CRBU UPTA)

for domain in "${DOMAINS[@]}"; do
    gdal_calc.py \
        -A /store/carroll/col/data/2025/mosaic/${domain}_2025_mosaic_rfl_rgb.tif \
        --allBands=A \
        --outfile=/store/carroll/col/data/2025/mosaic/tmp_uint16_${domain}.tif \
        --calc="A*10000" \
        --type=UInt16 \
        --overwrite

    gdal_translate \
        /store/carroll/col/data/2025/mosaic/tmp_uint16_${domain}.tif \
        /store/carroll/col/data/2025/mosaic/${domain}_2025_mosaic_rfl_rgb_small.tif \
        -of COG \
        -co COMPRESS=ZSTD \
        -co LEVEL=15 \
        -co BLOCKSIZE=512 \
        -co OVERVIEW_COMPRESS=ZSTD

    rm /store/carroll/col/data/2025/mosaic/tmp_uint16_${domain}.tif
done