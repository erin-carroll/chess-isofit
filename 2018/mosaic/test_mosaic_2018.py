import subprocess

# define filepaths
today = '20251108'
all_obs_files = '/store/carroll/col/data/2018/mosaic/test_obs_files.txt'
mosaic_glt_out = f'/store/carroll/col/data/2018/mosaic/test_neon_2018_mosaic_glt_{today}.tif'

# generate mosiac glt
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc {mosaic_glt_out} {all_obs_files} --x_resolution 1 --output_epsg 32613 --log_file /home/carroll/logs/test_mosaic_glt_{today}.log --n_cores 64 --criteria_band 5 --criteria_mode min'
print(cmd_str)
subprocess.run(cmd_str, shell=True)