from glob import glob
import os

for domain in ['ALMO', 'UPTA']: # , 'CRBU'

    tile_fps = glob(f'/store/carroll/col/data/2025/mosaic/glt_chunks/{domain}*.tif')
    
    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/glt_tiles_list_{domain}.txt'
    with open(fp_out, 'w') as f:
        for s in tile_fps:
            f.write(f'{s}\n')