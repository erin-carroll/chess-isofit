import os
from glob import glob
import numpy as np
import pyproj
from osgeo import osr, gdal
import rasterio
from rasterio.merge import merge
import spectral_util.spec_io as spec_io
import spectral_util.mosaic as mosaic

os.chdir('/store/carroll/col/data/2018/')

input_file_list = f'mosaic/file_lists/top_priority_isofit_obs.txt'
input_files = [x.strip() for x in open(input_file_list, 'r').readlines()]
# tile_fps = [x for x in glob('mosaic/neon_2018_mosaic_glt_3*.tif') if 'aligned' not in x]

tile_fps = [
    'mosaic/neon_2018_mosaic_glt_316122.5833512874_4306498.2403583685_323186.2164965977_4297525.547926542.tif',
    'mosaic/neon_2018_mosaic_glt_316127.5833512874_4315455.932790195_323181.2164965977_4306493.2403583685.tif',
    'mosaic/neon_2018_mosaic_glt_316127.5833512874_4324418.625222021_323181.2164965977_4315455.932790195.tif',
    'mosaic/neon_2018_mosaic_glt_323176.2164965977_4306498.2403583685_330239.849641908_4297525.547926542.tif',
    'mosaic/neon_2018_mosaic_glt_323181.2164965977_4315455.932790195_330234.849641908_4306493.2403583685.tif',
    'mosaic/neon_2018_mosaic_glt_323181.2164965977_4324418.625222021_330234.849641908_4315455.932790195.tif',
    'mosaic/neon_2018_mosaic_glt_330229.849641908_4306498.2403583685_337293.4827872183_4297525.547926542.tif',
    'mosaic/neon_2018_mosaic_glt_330229.849641908_4315460.932790195_337293.4827872183_4306488.2403583685.tif',
    'mosaic/neon_2018_mosaic_glt_330229.849641908_4324423.625222021_337293.4827872183_4315450.932790195.tif',
]

nodata=0

output_epsg = 32613
gproj = osr.SpatialReference()
gproj.ImportFromEPSG(int(output_epsg))
wkt = gproj.ExportToWkt()
proj = pyproj.Proj(f"epsg:{output_epsg}")

x_resolution = 1
y_resolution = -1

# construct full reference mosaic grid per build_obs_nc
ul_lr = mosaic.get_ul_lr_from_files(input_files, get_resolution=False)
ul = proj(ul_lr[0], ul_lr[1])
lr = proj(ul_lr[2], ul_lr[3])
ul_lr = [ul[0], ul[1], lr[0], lr[1]]
trans = [ul_lr[0] - x_resolution/2., x_resolution, 0, 
         ul_lr[1] - y_resolution/2., 0, y_resolution]
meta = spec_io.GenericGeoMetadata(['GLT X', 'GLT Y', 'File Index', 'OBS val'], 
                                  projection=wkt, 
                                  geotransform=trans, 
                                  pre_orthod=True, 
                                  nodata_value=nodata)
glt = np.ones(( int(np.ceil((ul_lr[3] - ul_lr[1]) / y_resolution)), 
                 int(np.ceil((ul_lr[2] - ul_lr[0]) / x_resolution)),
                 3), dtype=np.int32)
output_file = f'mosaic/reference_grid.tif'
spec_io.write_cog(output_file, glt, meta, nodata_value=nodata)

# warp each tile to the reference grid
print('warping tiles to reference grid...')
ref_fp = f'mosaic/reference_grid.tif'
ref = gdal.Open(ref_fp)
gt = ref.GetGeoTransform()
proj = ref.GetProjection()
xres = gt[1]
yres = abs(gt[5])
ref_ul_x = gt[0]
ref_ul_y = gt[3]
ref_lr_x = ref_ul_x + ref.RasterXSize * xres
ref_lr_y = ref_ul_y - ref.RasterYSize * yres
resample_alg = gdal.GRA_NearestNeighbour
warp_opts = gdal.WarpOptions(
    format="GTiff",
    dstSRS=proj,
    xRes=xres,
    yRes=yres,
    outputBounds=(ref_ul_x, ref_lr_y, ref_lr_x, ref_ul_y),
    targetAlignedPixels=True,
    resampleAlg=resample_alg,
    multithread=True,
    creationOptions=["TILED=YES", "COMPRESS=DEFLATE", "BIGTIFF=YES"],
)
aligned = []
for fp in tile_fps:
    fp_out = fp.replace('.tif', '_aligned.tif')
    gdal.Warp(str(fp_out), str(fp), options=warp_opts)
    aligned.append(fp_out)

# merge grid aligned tiles
print('merging aligned tiles...')
ds = [rasterio.open(fp) for fp in aligned]
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
fp_out = f'mosaic/CRBU_mosaic_glt_2018.tif'
with rasterio.open(fp_out, 'w', **out_meta) as dst:
    dst.write(mosaic)
for ds in ds:
    ds.close()
