import subprocess
import ast
import os
import argparse
import sys
from glob import glob

os.chdir('/store/carroll/col/data/2025/')

parser = argparse.ArgumentParser()
parser.add_argument("--domain", required=True)
args = parser.parse_args()
domain = args.domain

# define filepaths
mosaic_glt_tiles = glob(f'mosaic/glt_tiled/{domain}/{domain}_mosaic_glt_2025_*.tif')

all_rfl_files = f'mosaic/file_lists/top_priority_rfl_{domain}.txt'
all_unc_files = f'mosaic/file_lists/top_priority_unc_{domain}.txt'
citation_str = '/store/carroll/col/data/2025/mosaic/citation_str_2025.txt'

# check fps
for l in [all_rfl_files, all_unc_files]:
    with open(l, 'r') as f:
        fps = [line.strip() for line in f]
    for fp in fps:
        if not os.path.exists(fp):
            print(f'File does not exist: {fp}')
            sys.exit(1)  

# apply glt to generate mosaic
for glt_file in mosaic_glt_tiles:
    print(glt_file)

    fp_out = f'mosaic/mosaic_tiled/{domain}/{domain}_2025_mosaic_rfl_{os.path.basename(glt_file).split("2025_")[1].removesuffix(".tif")}.nc'

    # rfl
    cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {glt_file} {all_rfl_files} {fp_out} --output_format netcdf --variable_name reflectance --citation_str {citation_str}'
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)

    # unc
    cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {glt_file} {all_unc_files} {fp_out} --output_format netcdf --variable_name reflectance_uncertainty --citation_str {citation_str}'
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)