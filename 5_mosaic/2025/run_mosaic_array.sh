domain=ALMO
N=$(wc -l < /store/carroll/col/data/2025/mosaic/file_lists/${domain}_glt_tiles.txt)

# Start conservative to protect /store and nodes
K=4

sbatch --export=DOMAIN=${domain} --array=1-${N}%${K} /store/carroll/repos/chess-isofit/5_mosaic/2025/mosaic_array.sh