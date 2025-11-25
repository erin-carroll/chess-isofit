import subprocess
import os
from glob import glob

# define filepaths
today = '20251114'

home = '/store/carroll/col/data/2018/mosaic/'
all_obs_files = os.path.join(home, 'file_lists/top_priority_isofit_obs.txt')

# generate mosiac glt for each tile
ul_lr_grids = '/store/carroll/col/data/2018/mosaic/file_lists/ul_lr_grids.txt'
with open(ul_lr_grids, 'r') as f:
    ul_lr_grids = f.readlines()
ul_lr_grids = [ast.literal_eval(x.strip()) for x in ul_lr_grids]
    
for idx, ul_lr in enumerate(ul_lr_grids):
    mosaic_glt_out = os.path.join(home, f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt_{idx}.tif')
    cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc {mosaic_glt_out} {all_obs_files} --x_resolution 1 --output_epsg 32613 --target_extent_ul_lr {ul_lr[0]} {ul_lr[1]} {ul_lr[2]} {ul_lr[3]} --log_file /home/carroll/logs/mosaic_glt_{idx}_{today}.log --n_cores 64 --criteria_band 5 --criteria_mode min'
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)
