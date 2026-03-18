domain="UPTA"
year="2025"

N=$(wc -l < /store/carroll/col/data/${year}/mosaic/file_lists/${domain}_glt_tiles_new_rerun.txt)
K=4
sbatch --export=DOMAIN="${domain}",YEAR="${year}" --array=1-${N}%${K} /store/carroll/repos/chess-isofit/5_mosaic/2018/3_mosaic_array_2018_rerun.sh