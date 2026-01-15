import subprocess
import ast

# define filepaths
all_obs_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt'

mosaic_glt_out = '/store/carroll/col/data/2018/mosaic/CRBU_mosaic_glt_2018.tif'

all_rfl_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_refl.txt'
all_unc_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_unc.txt'
# all_ewt_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_ewt.txt'
all_ewt_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_ewt_pressureelevationtest.txt'
all_shade_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_shade.txt'

mosaic_rfl_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_rfl'
mosaic_unc_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_unc'
mosaic_obs_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_obs'
# mosaic_ewt_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_ewt'
mosaic_ewt_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_ewt_pressureelevationtest'
mosaic_shade_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_shade'


# apply glt to generate mosaics

# rfl
# n_channels = 426
# channels = list(range(n_channels))
# chunk_size = 25
# bands_list = [channels[x:x+chunk_size] for x in range(0, n_channels, chunk_size)]

# for b in range(n_channels):
#     fp_out = f'{mosaic_rfl_out}_{b}'
#     cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_rfl_files} {fp_out} --bands {b} --output_format envi'
#     print(cmd_str)
#     subprocess.run(cmd_str, shell=True)

# for i in range(len(bands_list)):
#     bands = bands_list[i]
#     band_arg_str = ' '.join(f'--bands {b}' for b in bands)
#     fp_out = f'{mosaic_rfl_out}_{bands[0]}'
#     cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_rfl_files} {fp_out} {band_arg_str} --output_format envi'
#     print(cmd_str)
#     subprocess.run(cmd_str, shell=True)

# # unc
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_unc_files} {mosaic_unc_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # ewt
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_ewt_files} {mosaic_ewt_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# obs
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_obs_files} {mosaic_obs_out} --output_format envi'
print(cmd_str)
subprocess.run(cmd_str, shell=True)

# shade
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_shade_files} {mosaic_shade_out} --output_format envi'
print(cmd_str)
subprocess.run(cmd_str, shell=True)