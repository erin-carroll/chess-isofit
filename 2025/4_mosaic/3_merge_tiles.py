import os
from glob import glob
import numpy as np
import pyproj
from osgeo import osr, gdal
import rasterio
from rasterio.merge import merge
import spectral_util.spec_io as spec_io
import spectral_util.mosaic as mosaic

os.chdir('/store/carroll/col/data/2025/')

domain = 'CRBU'
print(domain)

tile_fps = [x for x in glob(f'mosaic/{domain}_2025_mosaic_glt_*.tif')]

nodata=0

x_resolution = 1
y_resolution = -1

# merge grid aligned tiles
print('merging aligned tiles...')
ds = [rasterio.open(fp) for fp in tile_fps] # aligned
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
fp_out = f'mosaic/{domain}_mosaic_glt_2025_cloudshadow_rounded.tif'
with rasterio.open(fp_out, 'w', **out_meta) as dst:
    dst.write(mosaic)
for ds in ds:
    ds.close()
