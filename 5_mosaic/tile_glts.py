import os
import math
import rasterio
from rasterio.windows import Window
from rasterio.transform import Affine
import numpy as np

os.chdir('/store/carroll/col/data')

for domain in ['ALMO', 'CRBU', 'UPTA']:
    print(domain)
    for year in [2025]: # 2018, 
        fp_glt = f'{year}/mosaic/{domain}_mosaic_glt_{year}.tif'
        if not os.path.exists(fp_glt):
            continue
        print(domain, year)
        out_dir = f'{year}/mosaic/glt_tiled/{domain}/'
        os.makedirs(out_dir, exist_ok=True)

        tile_size = 1000
        nodata = 0
        res = 1

        with rasterio.open(fp_glt) as src:
            xmin, ymin, xmax, ymax = src.bounds
            x_start = math.floor(xmin / tile_size) * tile_size
            x_end = math.ceil(xmax / tile_size) * tile_size
            y_start = math.floor(ymin / tile_size) * tile_size
            y_end = math.ceil(ymax / tile_size) * tile_size

            profile = src.profile.copy()
            profile.update(
                width=tile_size,
                height=tile_size
            )

            n_tiles_x = int((x_end - x_start) / tile_size)
            n_tiles_y = int((y_end - y_start) / tile_size)

            print('x', n_tiles_x, 'y', n_tiles_y)

            for ty in range(n_tiles_y):
                print(ty)
                y_bot = y_start + ty * tile_size
                y_top = y_bot + tile_size

                for tx in range(n_tiles_x):
                    x_left = x_start + tx * 1000
                    x_right = x_left + 1000

                    tile_transform = Affine(res, 0, x_left, 0, -res, y_top)
                    
                    # get intersection of tile with source raster bounds
                    ixmin = max(x_left, xmin)
                    ixmax = min(x_right, xmax)
                    iymin = max(y_bot, ymin)
                    iymax = min(y_top, ymax)

                    # if no overlap
                    if ixmin >= ixmax or iymin >= iymax:
                        continue
                    
                    # get window in source raster coordinates
                    src_col0 = int(math.floor((ixmin - xmin) / res))
                    src_col1 = int(math.ceil((ixmax - xmin) / res))
                    src_row0 = int(math.floor((ymax - iymax) / res))   # iymax is top of overlap
                    src_row1 = int(math.ceil((ymax - iymin) / res))    # iymin is bottom of overlap

                    # clip to dataset bounds
                    src_col0 = max(0, min(src.width, src_col0))
                    src_col1 = max(0, min(src.width, src_col1))
                    src_row0 = max(0, min(src.height, src_row0))
                    src_row1 = max(0, min(src.height, src_row1))

                    win = Window(src_col0, src_row0, src_col1 - src_col0, src_row1 - src_row0)

                    # get dst window in tile coordinates (is this part unnecessary?)
                    dst_col0 = int(round((ixmin - x_left) / res))
                    dst_col1 = dst_col0 + int(win.width)
                    dst_row0 = int(round((y_top - iymax) / res))
                    dst_row1 = dst_row0 + int(win.height)

                    tile_arr = np.full((src.count, tile_size, tile_size), nodata, dtype=src.dtypes[0])
                    data = src.read(window=win, boundless=False)  # shape (bands, h, w)

                    # skip if all nodata
                    if np.all(data == nodata):
                        continue

                    # safety clip in case of rounding edge cases
                    h, w = data.shape[1], data.shape[2]
                    dst_row1 = min(tile_size, dst_row0 + h)
                    dst_col1 = min(tile_size, dst_col0 + w)
                    data = data[:, :dst_row1 - dst_row0, :dst_col1 - dst_col0]

                    tile_arr[:, dst_row0:dst_row1, dst_col0:dst_col1] = data
                    
                    # export
                    fp_out = os.path.join(out_dir, os.path.basename(fp_glt).replace('.tif', f'_{int(x_left)}_{int(y_bot)}.tif'))
                    profile.update(transform=tile_transform)
                    with rasterio.open(fp_out, "w", **profile) as dst:
                        dst.write(tile_arr)
