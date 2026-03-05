for list in \
    /store/carroll/col/data/2025/mosaic/file_lists/top_priority_rfl_ALMO.txt \
    /store/carroll/col/data/2025/mosaic/file_lists/top_priority_rfl_CRBU.txt \
    /store/carroll/col/data/2025/mosaic/file_lists/top_priority_rfl_UPTA.txt
do
    while IFS= read -r fp; do
        [[ -z "$fid" ]] && continue   # skip blank lines
        sbatch \
            --job-name=ewt_2025 \
            --nodes=1 \
            --cpus-per-task=64 \
            --partition=highcpu \
            --output=/home/carroll/logs/%j_%x.out \
            --error=/home/carroll/logs/%j_%x.err \
            --wrap="python /store/carroll/repos/chess-isofit/3_ewt/ewt.py --fp_rfl ${fp}"
    done < "$list"
done
