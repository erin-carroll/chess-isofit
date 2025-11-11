import subprocess

# define filepaths
today = '20251108'
all_obs_files = '/store/carroll/col/data/2018/mosaic/top_priority_isofit_obs.txt'
# all_rfl_files = '/store/carroll/col/data/2018/mosaic/top_priority_isofit_rfl.txt'
# all_unc_files = '/store/carroll/col/data/2018/mosaic/top_priority_isofit_unc.txt'
mosaic_glt_out = f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt_{today}.tif'
# mosaic_rfl_out = f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_rfl_{today}'
# mosaic_unc_out = f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_unc_{today}'
# mosaic_obs_out = f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_obs_{today}'

# generate mosiac glt
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc {mosaic_glt_out} {all_obs_files} --x_resolution 1 --output_epsg 32613 --log_file /home/carroll/logs/mosaic_glt_{today}.log --n_cores 64 --criteria_band 5 --criteria_mode min'
print(cmd_str)
subprocess.run(cmd_str, shell=True)

# # apply glt to generate mosaics

# # rfl
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_rfl_files} {mosaic_rfl_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # unc
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_unc_files} {mosaic_unc_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # obs
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_obs_files} {mosaic_obs_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)