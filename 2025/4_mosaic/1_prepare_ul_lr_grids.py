import pyproj
import spectral_util
import spectral_util.spec_io as spec_io
import spectral_util.mosaic as mosaic

for domain in ['ALMO','CRBU','UPTA']:

    input_file_list = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_obs_{domain}.txt'
    input_files = [x.strip() for x in open(input_file_list, 'r').readlines()]

    output_epsg = 32613
    proj = pyproj.Proj(f"epsg:{output_epsg}")

    ul_lr = mosaic.get_ul_lr_from_files(input_files, get_resolution=False)
    # convert to output epsg
    ul = proj(ul_lr[0], ul_lr[1])
    lr = proj(ul_lr[2], ul_lr[3])
    ul_lr = [round(v) for v in (ul[0], ul[1], lr[0], lr[1])]

    # tile grid
    n = 10

    xmin, ymax, xmax, ymin = ul_lr
    dx = round((xmax - xmin) / n)
    dy = round((ymax - ymin) / n)

    print(domain)
    print(ul_lr)
    print(dx, dy)

    lis_ul_lr = []
    for row in range(n):
        ul_y = ymax - row * dy + 5 # slight overlap
        lr_y = ymax - (row + 1) * dy - 5
        for col in range(n):
            ul_x = xmin + col * dx - 5 # slight overlap
            lr_x = xmin + (col + 1) * dx + 5
            lis_ul_lr.append([ul_x, ul_y, lr_x, lr_y])

    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/ul_lr_grids_{domain}.txt'
    with open(fp_out, 'w') as f:
        f.writelines(f'{x}\n' for x in lis_ul_lr)