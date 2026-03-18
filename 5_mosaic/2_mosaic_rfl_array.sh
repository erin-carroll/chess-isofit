#!/bin/bash
#SBATCH --job-name=applyglt
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=250G
#SBATCH --output=/home/carroll/logs/%x_%A_%a.out
#SBATCH --error=/home/carroll/logs/%x_%A_%a.err

set -euo pipefail

source /store/carroll/miniforge3/etc/profile.d/conda.sh
conda activate isofit_env

DOMAIN="$DOMAIN"

YEAR="$YEAR"

BASE="/store/carroll/col/data/${YEAR}"
cd "$BASE"

# prevent hidden threading storms
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

TILE_LIST="mosaic/file_lists/${DOMAIN}_glt_tiles.txt"
ALL_RFL="mosaic/file_lists/top_priority_rfl_${DOMAIN}.txt"
ALL_UNC="mosaic/file_lists/top_priority_unc_${DOMAIN}.txt"
CITATION_STR="mosaic/citation_str_${YEAR}.txt"

GLT_FILE="$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$TILE_LIST")"
echo "TASK ${SLURM_ARRAY_TASK_ID}: ${GLT_FILE}"

TILE_ID="$(basename "$GLT_FILE")"
TILE_ID="${TILE_ID##*_glt_}"
TILE_ID="${TILE_ID%.tif}"

OUT_DIR="mosaic/mosaic_tiled/${DOMAIN}"
FP_OUT="${OUT_DIR}/${DOMAIN}_${YEAR}_mosaic_rfl_${TILE_ID}.nc"

# ---- helper: true if variable already exists as a root variable in header ----
nc_has_var () {
  local fp="$1"
  local var="$2"
  local hdr
  if ! hdr="$(ncdump -h "$fp" 2>&1)"; then
    echo "WARNING: ncdump failed on $fp" >&2
    echo "$hdr" >&2
    return 1
  fi
  echo "$hdr" | grep -Eq "^[[:space:]]*(byte|char|short|int|long|float|double|ubyte|ushort|uint|int64|uint64)[[:space:]]+${var}[[:space:]]*\\("
}

if [[ -f "$FP_OUT" ]] && nc_has_var "$FP_OUT" "reflectance" && nc_has_var "$FP_OUT" "reflectance_uncertainty"; then
    echo "Output file already contains reflectance and reflectance_uncertainty, exiting early: $FP_OUT"
    exit 0
fi

if [[ -f "$FP_OUT" ]] && nc_has_var "$FP_OUT" "reflectance"; then
    echo "Skipping reflectance for $FP_OUT"
else
    echo "Applying GLT for reflectance: $FP_OUT"
    python -u /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt \
        "$GLT_FILE" "$ALL_RFL" "$FP_OUT" \
        --output_format netcdf \
        --variable_name reflectance \
        --citation_str "$CITATION_STR"
fi

if nc_has_var "$FP_OUT" "reflectance_uncertainty"; then
    echo "Skipping reflectance_uncertainty for $FP_OUT"
else
    echo "Applying GLT for reflectance_uncertainty: $FP_OUT"
    python -u /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt \
      "$GLT_FILE" "$ALL_UNC" "$FP_OUT" \
      --output_format netcdf \
      --variable_name reflectance_uncertainty \
      --citation_str "$CITATION_STR"
fi

echo "SUCCESS: $FP_OUT"