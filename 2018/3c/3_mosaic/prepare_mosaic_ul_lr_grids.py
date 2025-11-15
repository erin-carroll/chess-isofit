import pyproj

import sys
sys.path.append('/store/carroll/repos/SpectralUtil/spectral_util')
import spec_io, mosaic

input_file_list = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt'
input_files = [x.strip() for x in open(input_file_list, 'r').readlines()]

output_epsg = 32613
proj = pyproj.Proj(f"epsg:{output_epsg}")

ul_lr = mosaic.get_ul_lr_from_files(input_files, get_resolution=False)
# convert to output epsg
ul = proj(ul_lr[0], ul_lr[1])
lr = proj(ul_lr[2], ul_lr[3])
ul_lr = [ul[0], ul[1], lr[0], lr[1]]

# split into 9 ul_lr chunks
n = 3

xmin, ymax, xmax, ymin = ul_lr
dx = (xmax - xmin) / n
dy = (ymax - ymin) / n

lis_ul_lr = []
for row in range(n):
    ul_y = ymax - row * dy
    lr_y = ymax - (row + 1) * dy
    for col in range(n):
        ul_x = xmin + col * dx
        lr_x = xmin + (col + 1) * dx
        lis_ul_lr.append([ul_x, ul_y, lr_x, lr_y])

fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/ul_lr_grids.txt'
with open(fp_out, 'w') as f:
    f.writelines(f'{x}\n' for x in lis_ul_lr)





