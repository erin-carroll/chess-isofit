import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping
import rasterio
from rasterio.features import rasterize
import numpy as np
from osgeo import gdal
from glob import glob
import argparse
import ray
import sys

# set up parser so flight id submitted from batch script
parser = argparse.ArgumentParser()
parser.add_argument("--fid", required=True)
args = parser.parse_args()
fid = args.fid
print(fid)

year = fid[6:10]
if year=='2025':
    fid = fid[:21]

nodatavalue = -9999

fp_rfl = glob(f'/store/carroll/col/data/{year}/deploy_6c_20260214/{fid}*/output/{fid}_rfl')[0]
fp_unc = glob(f'/store/carroll/col/data/{year}/deploy_6c_20260214/{fid}*/output/{fid}_uncert')[0]
fp_shade = glob(f'/store/carroll/col/data/{year}/shade/{fid}*shade.tif')[0]
if year=='2025':
    fp_loc = glob(f'/store/carroll/col/data/{year}/raw/L1/radianceENVI/{fid}*_IGM_Data')[0]
    fp_poly = '/store/carroll/col/data/extractions/crown_delineation_Tree_all.geojson'
else:
    fp_loc = glob(f'/store/carroll/col/data/{year}/raw/L1/*/{fid}_rdn_ort_igm_ort')[0]
    fp_poly = '/store/carroll/col/data/extractions/CRBU2018_AOP_Crowns.geojson'

if any(not os.path.exists(fp) for fp in [fp_rfl, fp_unc, fp_shade, fp_loc]):
    print(f'missing input rasters for fid {fid}, exiting')
    sys.exit(1)

# rasterize crown polygons (burning in site_number) to create mask for data extraction
gdf = gpd.read_file(fp_poly)
gdf = gdf.rename(columns={'id': 'site_number'})
gdf['site_number'] = gdf.site_number.astype(float)
shapes = [(mapping(geom), val) for geom, val in zip(gdf.geometry, gdf.site_number)]
with rasterio.open(fp_loc) as src:
    mask = rasterize(shapes, out_shape=(src.height, src.width), transform=src.transform, all_touched=False, nodata=nodatavalue, fill=nodatavalue)
    nodata = src.read(1)==nodatavalue
mask[nodata] = nodatavalue
rows, cols = np.where(mask!=nodatavalue)
vals = mask[mask!=nodatavalue] # site numbers

if len(rows) == 0:
    print(f'no valid px found for fid {fid}, exiting')
    sys.exit(1)
else:
    print(f'{vals.shape[0]} px within fid {fid} for data extraction')

# extract data per pixel
all_x = []
all_y = []
all_rfl = []
all_unc = []
all_shade = []

@ray.remote
def single_read(i):
    row = rows[i]
    col = cols[i]
    xy = gdal.Open(fp_loc,gdal.GA_ReadOnly).ReadAsArray(col,row,1,1)
    x_utm = xy[0,0,0]
    y_utm = xy[1,0,0]
    rfl_dat = gdal.Open(fp_rfl, gdal.GA_ReadOnly).ReadAsArray(col,row,1,1).reshape(1,-1)
    unc_dat = gdal.Open(fp_unc, gdal.GA_ReadOnly).ReadAsArray(col,row,1,1).reshape(1,-1)
    shade_dat = gdal.Open(fp_shade,gdal.GA_ReadOnly).ReadAsArray(col,row,1,1)[0,0]
    return x_utm, y_utm, rfl_dat, unc_dat, shade_dat

print('executing individual retrievals')
ray.init()
results = []
for _i in range(rows.shape[0]):
    results.append(single_read.remote(_i)) 
output = [ray.get(jid) for jid in results]

del results
for o in output:
    if o is not None:
        all_x.extend([o[0]])
        all_y.extend([o[1]])
        all_rfl.extend(o[2])
        all_unc.extend(o[3])
        all_shade.extend([o[4]])
del output

all_x = np.vstack(all_x)
all_y = np.vstack(all_y)
all_rfl = np.vstack(all_rfl)
all_unc = np.vstack(all_unc)
all_shade = np.vstack(all_shade)

print('exporting csv')
csv_dat = np.append(vals[:, None],rows[:, None],axis=-1)
csv_dat = np.append(csv_dat,cols[:, None],axis=-1)
csv_dat = np.append(csv_dat,all_x,axis=-1)
csv_dat = np.append(csv_dat,all_y,axis=-1)
csv_dat = np.append(csv_dat,all_shade,axis=-1)
csv_dat = np.append(csv_dat,all_rfl,axis=-1)
csv_dat = np.append(csv_dat,all_unc,axis=-1)

header = ['site_number','row', 'col', 'x_utm','y_utm', 'shade']
header = header + [f'rfl_band_{b}' for b in range(1,427)]
header = header + [f'unc_band_{b}' for b in range(1,427)]
df = pd.DataFrame(data=csv_dat, columns=header)
df['fid'] = fid
if year=='2025':
    df = df.merge(gdf[['site_number','domain', 'sampling_area', 'site_type']], on='site_number', how='left')
    df = df[['site_number','domain','sampling_area','site_type', 'fid'] + [c for c in df.columns if c not in ['site_number','domain','sampling_area','site_type', 'fid']]] # reorder columns
else:
    df = df[['site_number','fid'] + [c for c in df.columns if c not in ['site_number','fid']]] # reorder columns
print('df shape:', df.shape)

fp_out = f'/store/carroll/col/data/extractions/csv/{fid}_extraction.csv'
df.to_csv(fp_out, index=False)
print('done')