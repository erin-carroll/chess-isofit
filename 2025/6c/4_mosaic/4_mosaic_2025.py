import subprocess
import ast
import os
import argparse

os.chdir('/store/carroll/col/data/2025/')

parser = argparse.ArgumentParser()
parser.add_argument("--domain", required=True)
args = parser.parse_args()
domain = args.domain

# define filepaths
mosaic_glt = f'mosaic/{domain}_mosaic_glt_2025.tif'

all_obs_files = f'mosaic/file_lists/top_priority_obs_{domain}.txt'
all_shade_files = f'mosaic/file_lists/top_priority_shade_{domain}.txt'

mosaic_obs_out = f'mosaic/{domain}_mosaic_obs_2025'
mosaic_shade_out = f'mosaic/{domain}_mosaic_shade_2025'

# apply glt to generate mosaics

# # obs
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_obs_files} {mosaic_obs_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# shade
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_shade_files} {mosaic_shade_out} --output_format envi'
print(cmd_str)
subprocess.run(cmd_str, shell=True)