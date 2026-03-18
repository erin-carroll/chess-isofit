import os
from glob import glob
import numpy as np
import pyproj
from osgeo import osr, gdal
import rasterio
from rasterio.merge import merge
import spectral_util.spec_io as spec_io
import spectral_util.mosaic as mosaic

nodata=0

for year in ['2025', '2018']:
    os.chdir(f'/store/carroll/col/data/{year}/')

    for domain in ['ALMO', 'CRBU', 'UPTA']:
        tile_fps = [x for x in glob(f'mosaic/glt_tiled/{domain}/{domain}_{year}_mosaic_glt_*.tif')]
        if len(tile_fps)<1:
            continue

        print(domain)
        print(f'n tiles: {len(tile_fps)}')

        # filtering out all nodata tiles from matching 2025 grid
        keep_fps = []
        for fp in tile_fps:
            with rasterio.open(fp) as src:
                b3 = src.read(3, masked=False)
                if not np.all(b3 == nodata):
                    keep_fps.append(fp)
                else:
                    os.remove(fp)
                    print('deleted ', fp)
        print(f'keeping {len(keep_fps)} tiles')

        # merge grid aligned tiles
        print('merging aligned tiles...')
        ds = [rasterio.open(fp) for fp in keep_fps] # aligned
        mosaic, transform = merge(ds, method='first', nodata=nodata)
        print(f'out mosaic shape: {mosaic.shape}')
        out_meta = ds[0].meta.copy()
        out_meta.update({
            'height': mosaic.shape[1],
            'width': mosaic.shape[2],
            'transform': transform,
            'compress': 'DEFLATE',
            'tiled': True,
            'blockxsize': 512,
            'blockysize': 512,
        })
        fp_out = f'mosaic/{domain}_mosaic_glt_{year}.tif'
        with rasterio.open(fp_out, 'w', **out_meta) as dst:
            dst.write(mosaic)
        for ds in ds:
            ds.close()
