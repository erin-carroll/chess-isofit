list=/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_refl.txt

while IFS= read -r fp; do
    [[ -z "$fid" ]] && continue
    sbatch \
        --job-name=ewt_2018 \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=highcpu \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="python /store/carroll/repos/chess-isofit/3_ewt/ewt.py --fp_rfl ${fp}"
done < "$list"