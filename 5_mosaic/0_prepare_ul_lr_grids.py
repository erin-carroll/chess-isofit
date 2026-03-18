import pyproj
import spectral_util
import spectral_util.spec_io as spec_io
import spectral_util.mosaic as mosaic
import math

tile_size = 1000
nodata = 0
res = 1
output_epsg = 32613

for domain in ['ALMO', 'CRBU', 'UPTA']:
    print(domain)

    # get full extent ul_lr
    input_file_list = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_obs_{domain}.txt'
    input_files = [x.strip() for x in open(input_file_list, 'r').readlines()]
    proj = pyproj.Proj(f"epsg:{output_epsg}")
    ul_lr = mosaic.get_ul_lr_from_files(input_files, get_resolution=False)
    # convert to output epsg
    ul = proj(ul_lr[0], ul_lr[1])
    lr = proj(ul_lr[2], ul_lr[3])
    # round to nearest integer
    ul_lr = [round(v) for v in (ul[0], ul[1], lr[0], lr[1])]

    # round to thousands to match neon tiles
    ul_lr[0] = math.floor(ul_lr[0] / 1000) * 1000
    ul_lr[1] = math.ceil(ul_lr[1] / 1000) * 1000
    ul_lr[2] = math.ceil(ul_lr[2] / 1000) * 1000
    ul_lr[3] = math.floor(ul_lr[3] / 1000) * 1000

    # half pixel adjustment to match NEON grid
    ul_lr[0] += 0.5
    ul_lr[1] -= 0.5
    ul_lr[2] += 0.5
    ul_lr[3] -= 0.5

    xmin, ymax, xmax, ymin = ul_lr
    print(ul_lr)
    print(xmin, ymax, xmax, ymin)

    dx, dy = 1000, 1000
    print(dx, dy)

    lis_ul_lr = []

    n_row = math.ceil((ymax - ymin) / dy)
    n_col = math.ceil((xmax - xmin) / dx)

    print(n_row, n_col)

    for row in range(n_row):
        ul_y = ymax - row * dy
        lr_y = ymax - (row + 1) * dy
        for col in range(n_col):
            ul_x = xmin + col * dx
            lr_x = xmin + (col + 1) * dx
            lis_ul_lr.append([ul_x, ul_y, lr_x, lr_y])

    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/ul_lr_grids_{domain}.txt'
    with open(fp_out, 'w') as f:
        f.writelines(f'{x}\n' for x in lis_ul_lr)
    print('done', fp_out)