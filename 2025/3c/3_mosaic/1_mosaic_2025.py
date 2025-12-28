import subprocess
import ast

domain = 'UPTA'

# define filepaths
all_obs_files = f'/store/carroll/repos/chess-isofit/2025/3c/3_mosaic/top_priority_obs_{domain}.txt'
deprioritize_obs_files = f'/store/carroll/repos/chess-isofit/2025/3c/3_mosaic/deprioritize_obs.txt'
mosaic_glt_out = f'/store/carroll/col/data/2025/mosaic/neon_2025_mosaic_glt_{domain}.tif'

# create joint glt from priority obs files (min phase angle)
log_file=f'/home/carroll/logs/mosaic_glt_2025_{domain}.log'
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc {mosaic_glt_out} {all_obs_files} --deprioritize_file_list {deprioritize_obs_files} --x_resolution 1 --output_epsg 32613 --log_file {log_file} --n_cores 64 --criteria_band 5 --criteria_mode min'
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc {mosaic_glt_out} {all_obs_files} --x_resolution 1 --output_epsg 32613 --log_file {log_file} --n_cores 64 --criteria_band 5 --criteria_mode min'
print(cmd_str) 
subprocess.run(cmd_str, shell=True)