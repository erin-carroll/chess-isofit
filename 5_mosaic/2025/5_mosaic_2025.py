import subprocess
import ast
import os
import argparse
import sys

os.chdir('/store/carroll/col/data/2025/')

parser = argparse.ArgumentParser()
parser.add_argument("--domain", required=True)
args = parser.parse_args()
domain = args.domain

# define filepaths
mosaic_glt = f'mosaic/{domain}_mosaic_glt_2025.tif'

all_obs_files = f'mosaic/file_lists/top_priority_obs_{domain}.txt'
all_shade_files = f'mosaic/file_lists/top_priority_shade_{domain}.txt'
all_rfl_files = f'mosaic/file_lists/top_priority_rfl_{domain}.txt'
# all_ewt_files = f'mosaic/file_lists/top_priority_ewt_{domain}.txt'

mosaic_obs_out = f'mosaic/{domain}_2025_mosaic_obs.tif'
mosaic_shade_out = f'mosaic/{domain}_2025_mosaic_shade.tif'
mosaic_rgb_out = f'mosaic/{domain}_2025_mosaic_rfl_rgb.tif'
# mosaic_ewt_out = f'mosaic/{domain}_2025_mosaic_ewt.tif'

# quickly check fps
for l in [all_obs_files, all_shade_files, all_rfl_files]: # all_ewt_files
    with open(l, 'r') as f:
        fps = [line.strip() for line in f]
    for fp in fps:
        if not os.path.exists(fp):
            print(f'File does not exist: {fp}')
            sys.exit(1)

# apply glt to generate mosaics

# obs
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_obs_files} {mosaic_obs_out} --output_format tif'
print(cmd_str)
subprocess.run(cmd_str, shell=True)

# shade
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_shade_files} {mosaic_shade_out} --output_format tif'
print(cmd_str)
subprocess.run(cmd_str, shell=True)

# rgb
r = 58
g = 34
b = 19
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_rfl_files} {mosaic_rgb_out} --output_format tif --bands {r} --bands {g} --bands {b}'
print(cmd_str)
subprocess.run(cmd_str, shell=True)

# # ewt
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_ewt_files} {mosaic_ewt_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)