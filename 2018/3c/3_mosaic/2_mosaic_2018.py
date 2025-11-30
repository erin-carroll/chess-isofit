import subprocess
import ast

# define filepaths
all_obs_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt'
glt_files = '/store/carroll/col/data/2018/mosaic/file_lists/joint_glt_file_list.txt'
obs_file_lists = '/store/carroll/col/data/2018/mosaic/file_lists/joint_obs_file_list.txt'

mosaic_glt_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt.tif'
output_file_list = '/store/carroll/col/data/2018/mosaic/file_lists/neon_2018_mosaic_joint_glt.txt'

ul_lr_grids = '/store/carroll/col/data/2018/mosaic/file_lists/ul_lr_grids.txt'

all_rfl_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_refl.txt'
all_unc_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_unc.txt'
all_ewt_files = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_ewt.txt'

mosaic_rfl_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_rfl'
mosaic_unc_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_unc'
mosaic_obs_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_obs'
mosaic_ewt_out = '/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_ewt'

# # merge tiled glts
# xs, ys = [], []
# with open(ul_lr_grids) as f:
#     for line in f:
#         ulx, uly, lrx, lry = ast.literal_eval(line)
#         xs.append(ulx); xs.append(lrx)
#         ys.append(uly); ys.append(lry)
# ul_lr = (min(xs), max(ys), max(xs), min(ys))

# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py merge-joint-glts {mosaic_glt_out} {glt_files} --x_resolution 1 --output_epsg 32613 --target_extent_ul_lr {ul_lr[0]} {ul_lr[1]} {ul_lr[2]} {ul_lr[3]} --log_file /home/carroll/logs/stack_glt.log --n_cores 64'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# apply glt to generate mosaics

# rfl
# n_channels = 426
n_channels = 400
channels = list(range(n_channels))
chunk_size = 25
bands_list = [channels[x:x+chunk_size] for x in range(0, n_channels, chunk_size)]

# for b in range(n_channels):
#     fp_out = f'{mosaic_rfl_out}_{b}'
#     cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_rfl_files} {fp_out} --bands {b} --output_format envi'
#     print(cmd_str)
#     subprocess.run(cmd_str, shell=True)

for i in range(len(bands_list)):
    bands = bands_list[i]
    band_arg_str = ' '.join(f'--bands {b}' for b in bands)
    fp_out = f'{mosaic_rfl_out}_{bands[0]}'
    cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_rfl_files} {fp_out} {band_arg_str} --output_format envi'
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)

# unc
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_unc_files} {mosaic_unc_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # ewt
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_ewt_files} {mosaic_ewt_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)

# # obs
# cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py apply-glt {mosaic_glt_out} {all_obs_files} {mosaic_obs_out} --output_format envi'
# print(cmd_str)
# subprocess.run(cmd_str, shell=True)