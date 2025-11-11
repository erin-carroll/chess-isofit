import sys
sys.path.append('/store/carroll/repos/neon-isofit/')
from h5_to_envi import radianceH5toEnvi
import os
from glob import glob
import rasterio
from rasterio.merge import merge
import pandas as pd
import subprocess

home = '/store/carroll/col/data/2025/'
domains = ['2025_ALMO_1', '2025_CRBU_2', '2025_UPTA_1']

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

rasterName = 'Reflectance'

tiles = pd.read_csv('/store/carroll/col/data/2025/utm_grids_plots.csv') # identify grids that overlap plots

# convert rfl h5 to envi for relevant grids
# for domain in domains:
#     h5_dir = os.path.join(home, f'raw/L3/spectrometer/reflectance/{domain}/')
#     d_name = domain.split('_')[1] 
#     outDir = os.path.join(home, f'raw/L3/reflectanceENVI/{d_name}/')
#     os.makedirs(outDir, exist_ok=True)
    
#     # filter to grids that overlap plots
#     tiles_ = tiles[tiles['domain']==d_name]
#     h5_files = []
#     for x, y in zip(tiles_['centroid_x_rounded'], tiles_['centroid_y_rounded']):
#         fn = os.path.join(h5_dir, f'NEON_D13_{d_name}_DP3_{x}_{y}_bidirectional_reflectance.h5')
#         h5_files.append(fn)
    
#     for h5_filename in h5_files:
#         outFile = os.path.join(outDir,os.path.basename(h5_filename).removesuffix('.h5'))
#         try:
#             radianceH5toEnvi.convertH5RasterToEnvi(h5_filename, rasterName, outFile, filePathToEnviProjCs)
#         except:
#             print('failed', outFile)

# # download chm, dsm for each tile
# for domain in domains:
#     d_name = domain.split('_')[1]
#     tiles_ = tiles[tiles['domain']==d_name] # filter to grids that overlap plots
#     for x, y in zip(tiles_['centroid_x_rounded'], tiles_['centroid_y_rounded']):
#         # chm
#         cmd = f'rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/{domain}/L3/DiscreteLidar/CanopyHeightModelGtif/NEON_D13_{d_name}_DP3_{x}_{y}_CHM.tif /store/carroll/col/data/2025/raw/L3/discreteLidar/CHM/{d_name}/ --progress'
#         print(cmd)
#         subprocess.run(cmd, shell=True)

#         # dsm
#         cmd = f'rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/{domain}/L3/DiscreteLidar/DSMGtif/NEON_D13_{d_name}_DP3_{x}_{y}_DSM.tif /store/carroll/col/data/2025/raw/L3/discreteLidar/DSM/{d_name}/ --progress'
#         print(cmd)
#         subprocess.run(cmd, shell=True)

# function to mosaic
def mosaic_tiles(d_name, fps, fp_out, band_indices):
    srcs = [rasterio.open(fp) for fp in fps]
    mosaic, out_transform = merge(srcs, indexes=band_indices)
    meta = srcs[0].meta.copy()
    meta.update(
        driver="GTiff",
        height=mosaic.shape[1],
        width=mosaic.shape[2],
        count=len(band_indices),
        transform=out_transform,
        compress='DEFLATE',
        predictor=2,
        tiled=True)
    with rasterio.open(fp_out, 'w', **meta) as dst:
        dst.write(mosaic)
    for src in srcs:
        src.close()    

# mosaic rgb
band_indices = [60, 40, 30]
for domain in domains:
    d_name = domain.split('_')[1]
    fps = [x for x in glob(os.path.join(home, f'raw/L3/reflectanceENVI/{d_name}/*')) if '.' not in x]
    fp_out = os.path.join(home, f'raw/L3/reflectanceENVI/CHESS25_{d_name}_reflectance_rgb.tif')
    mosaic_tiles(d_name, fps, fp_out, band_indices)
    
# mosaic false color
band_indices = [80, 60, 40]
for domain in domains:
    d_name = domain.split('_')[1]
    fps = [x for x in glob(os.path.join(home, f'raw/L3/reflectanceENVI/{d_name}/*')) if '.' not in x]
    fp_out = os.path.join(home, f'raw/L3/reflectanceENVI/CHESS25_{d_name}_reflectance_falsecolor.tif')
    mosaic_tiles(d_name, fps, fp_out, band_indices)

# mosaic CHM
band_indices = [1] 
for domain in domains:
    d_name = domain.split('_')[1]
    fps = [x for x in glob(os.path.join(home, f'raw/L3/discreteLidar/CHM/{d_name}/*'))]
    fp_out = os.path.join(home, f'raw/L3/discreteLidar/CHM/CHESS25_{d_name}_CHM.tif') 
    mosaic_tiles(d_name, fps, fp_out, band_indices)

# mosaic DSM
band_indices = [1] 
for domain in domains:
    d_name = domain.split('_')[1]
    fps = [x for x in glob(os.path.join(home, f'raw/L3/discreteLidar/DSM/{d_name}/*'))]
    fp_out = os.path.join(home, f'raw/L3/discreteLidar/DSM/CHESS25_{d_name}_DSM.tif') 
    mosaic_tiles(d_name, fps, fp_out, band_indices)