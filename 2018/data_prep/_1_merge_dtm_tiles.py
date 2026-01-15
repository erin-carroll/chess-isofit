import os
from glob import glob
import numpy as np
import pyproj
from osgeo import osr, gdal
import rasterio
from rasterio.merge import merge
import spectral_util.spec_io as spec_io
import spectral_util.mosaic as mosaic

os.chdir('/store/carroll/col/data/2018/raw/L3/discreteLidar/DTM')

tile_fps = [x for x in glob('*.tif') if 'mosaic' not in x]
print(len(tile_fps), 'tiles found')

nodata=-9999

# merge grid aligned tiles
print('merging aligned tiles...')
ds = [rasterio.open(fp) for fp in tile_fps]
mosaic, transform = merge(ds, method='first', nodata=nodata)
out_meta = ds[0].meta.copy()
out_meta.update({
    'height': mosaic.shape[1],
    'width': mosaic.shape[2],
    'transform': transform,
    'compress': 'DEFLATE',
    'tiled': True,
    'BIGTIFF': 'YES',
})
fp_out = 'dtm_mosaic_crbu_2018.tif'
with rasterio.open(fp_out, 'w', **out_meta) as dst:
    dst.write(mosaic)
for ds in ds:
    ds.close()
