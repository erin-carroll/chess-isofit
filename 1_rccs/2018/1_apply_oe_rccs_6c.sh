FID_FILES=(
  /store/carroll/repos/chess-isofit/2018/6c/0_rccs/cal_tarp_fids.txt
  /store/carroll/repos/chess-isofit/2018/6c/0_rccs/bright_dark_fids.txt
)

for f in "${FID_FILES[@]}"; do
  while IFS= read -r fid; do
    [[ -z "$fid" ]] && continue
    sbatch \
        --job-name=rccs_6c_${fid} \
        --nodes=1 \
        --cpus-per-task=64 \
        --partition=standard \
        --output=/home/carroll/logs/%j_%x.out \
        --error=/home/carroll/logs/%j_%x.err \
        --wrap="python /store/carroll/repos/chess-isofit/1_rccs/2018/1_apply_oe_rccs_6c.py --fid ${fid}"
  done < "$f"
done