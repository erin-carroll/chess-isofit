list=/store/carroll/col/data/2018/mosaic/file_lists/crbu_2018_fids.txt

while IFS= read -r fid; do
    [[ -z "$fid" ]] && continue   # skip blank lines
    sbatch \
        --job-name="shade_${fid}" \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=patient \
        --mem=300G \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="python /store/carroll/repos/chess-isofit/4_shade/calculate_shade.py --fid ${fid} --solar_azimuth_band 4 --solar_zenith_band 5 --output_folder /store/carroll/col/data/2018/shade"
done < "$list"