import os
from glob import glob
import geopandas as gpd
import rasterio
from shapely.geometry import mapping
from rasterio.features import rasterize
import numpy as np

os.chdir('/store/carroll/col/data/2025/')

fps = glob('mosaic/cloud_shadow_masks/*.geojson')

for fp in fps:
    fid = fp.split('/')[-1].split('.')[0].split('_')
    domain = fid[0]
    date = fid[5]
    line = fid[6]
    print(fp)
    print(domain, date, line)
    fp_out = fp.removesuffix('.geojson')
    fp_ref = glob(f'raw/L1/radianceENVI/*{date}*{domain}*{line}*IGM_Data')[0]
    print(fp_ref, '\n')

    mask_geojson = gpd.read_file(fp)
    mask_shapes = [mapping(geom) for geom in mask_geojson.geometry]

    with rasterio.open(fp_ref) as ref_meta:
        mask_raster = rasterize(
            shapes=mask_shapes,
            out_shape=(ref_meta.shape[0], ref_meta.shape[1]),
            transform=ref_meta.transform,
            fill=0,
            all_touched=True,
        )
        out_meta = ref_meta.meta.copy()
    out_meta.update({
        'driver': 'ENVI',
        'count': 1,
    })

    with rasterio.open(fp_out, 'w', **out_meta) as dst:
        dst.write(mask_raster, 1)