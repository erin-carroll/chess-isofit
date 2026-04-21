import subprocess
import ast
import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--domain", required=True)
parser.add_argument("--year", required=True)
args = parser.parse_args()
domain = args.domain
year = args.year

os.chdir(f'/store/carroll/col/data/{year}/')

# define filepaths
mosaic_glt = f'mosaic/{domain}_{year}_mosaic_glt.tif'

all_obs_files = f'mosaic/file_lists/top_priority_obs_{domain}.txt'
all_shade_files = f'mosaic/file_lists/top_priority_shade_{domain}.txt'
all_rfl_files = f'mosaic/file_lists/top_priority_rfl_{domain}.txt'
all_ewt_files = f'mosaic/file_lists/top_priority_ewt_{domain}.txt'

mosaic_obs_out = f'mosaic/{domain}_{year}_mosaic_obs.tif'
mosaic_shade_out = f'mosaic/{domain}_{year}_mosaic_shade.tif'
mosaic_rgb_out = f'mosaic/{domain}_{year}_mosaic_rfl_rgb.tif'
mosaic_falsecolor_out = f'mosaic/{domain}_{year}_mosaic_rfl_falsecolor.tif'
mosaic_ewt_out = f'mosaic/{domain}_{year}_mosaic_ewt.tif'

# quickly check fps
for l in [all_shade_files]: #  all_obs_files, all_ewt_files, all_rfl_files
    with open(l, 'r') as f:
        fps = [line.strip() for line in f]
    for fp in fps:
        if not os.path.exists(fp):
            print(f'File does not exist: {fp}')
            sys.exit(1)

# apply glt to generate mosaics

# # obs
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_obs_files} {mosaic_obs_out} --output_format tif'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# shade
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_shade_files} {mosaic_shade_out} --output_format tif'
print(cmd_str)
subprocess.run(cmd_str, shell=True)

# # rgb
# r = 58
# g = 34
# b = 19
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_rfl_files} {mosaic_rgb_out} --output_format tif --bands {r} --bands {g} --bands {b}'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # false color
# r = 58
# g = 34
# nir = 89
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_rfl_files} {mosaic_falsecolor_out} --output_format tif --bands {nir} --bands {r} --bands {g}'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # ewt
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt} {all_ewt_files} {mosaic_ewt_out} --output_format tif'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)