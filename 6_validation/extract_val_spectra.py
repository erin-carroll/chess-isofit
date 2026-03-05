import os
from glob import glob
import pandas as pd
import geopandas as gpd
import numpy as np
from spectral.io import envi
from tqdm import tqdm

import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin

from shapely.geometry import mapping
import h5py

os.chdir('/store/carroll/col/data/2025/')

insitu = pd.read_csv('insitu/insitu_validation_target_mean.csv')
wvl_cols = [x for x in insitu.columns if x not in ['file_tag','date','site','utm_x','utm_y']]
    
wl_neon = np.loadtxt('/store/carroll/col/data/wavelengths_neon.txt')[:,1]*1000 # nm
wvl_col_neon = [f'w{x}' for x in wl_neon]

gdf = gpd.read_file('insitu/insitu_delineation_2025.geojson')
gdf = gdf.rename(columns={'fid':'idx'})
fids = gdf.flight.unique()

# extract isofit 6c rfl
out = []
for fid in tqdm(fids):
    tmp = gdf[gdf['flight']==fid] # filter raster_plot_event to a single fid

    # rasterize filtered gdf
    fp = glob(os.path.join('deploy_6c_20260214', f'{fid}_*', 'output', f'{fid}_rfl'))[0]
    line_id = fp.split('/')[1].split('_')[-1]
    gdf.loc[gdf['flight']==fid, 'line_id'] = line_id
    shapes = [(mapping(geom), val) for geom, val in zip(tmp.geometry, tmp.idx)]
    with rasterio.open(fp) as src:
        r = rasterize(shapes, out_shape=(src.height, src.width), transform=src.transform, all_touched=False, nodata=-9999, fill=-9999)

    # extract spectra
    mask = r!=-9999
    rfl = envi.open(fp+'.hdr').open_memmap()[mask]
    unc = envi.open(fp.replace('rfl', 'uncert')+'.hdr').open_memmap()[mask]
    val = r[mask]
    df = pd.DataFrame({
        'idx': val,
        'fid': fid})

    # export
    df_rfl = pd.DataFrame(rfl, columns=[f'rfl_{x}' for x in wvl_col_neon])
    df_unc = pd.DataFrame(unc, columns=[f'unc_{x}' for x in wvl_col_neon])
    df = pd.concat([df, df_rfl, df_unc], axis=1)
    out.append(df)
    
out_table = pd.concat(out)
out_table = out_table.merge(gdf[['target', 'idx']], on='idx', how='left')
fp_out = 'validation/rfl_insitu_deploy6c20260214.csv'
out_table.to_csv(fp_out, index=False)

# neon hrdf
out = []
for fid in tqdm(fids):
    tmp = gdf[gdf['flight']==fid] # filter raster_plot_event to a single fid
    shapes = [(mapping(geom), val) for geom, val in zip(tmp.geometry, tmp.idx)]
    
    # rasterize filtered gdf
    day = fid.split('_')[1]
    line_id = tmp['line_id'].unique()[0]
    fp = f'raw/L1/directionalReflectanceH5/NEON_D13_CRBU_DP1_{line_id}_{day}_directional_reflectance.h5'
    rfl = h5py.File(fp, 'r')['CRBU']['Reflectance']['Reflectance_Data']
    nrow = rfl.shape[0]
    ncol = rfl.shape[1]
    # get transform
    gt = h5py.File(fp, 'r')['CRBU/Reflectance/Metadata/Coordinate_System/Map_Info'][()].decode("utf-8", errors="ignore")
    parts = [p.strip() for p in gt.split(",")]
    ulx  = float(parts[3])
    uly  = float(parts[4])
    xres = float(parts[5])
    yres = float(parts[6])
    transform = from_origin(ulx, uly, xres, yres)
    r = rasterize(shapes, out_shape=(nrow, ncol), transform=transform, all_touched=False, nodata=-9999, fill=-9999)
    mask = r!=-9999

    # extract spectra
    rows, cols = np.where(mask)    
    rows = np.asarray(rows)
    cols = np.asarray(cols)
    r0, r1 = rows.min(), rows.max()
    c0, c1 = cols.min(), cols.max()
    window = rfl[r0:r1+1, c0:c1+1, :] 
    rr = rows - r0
    cc = cols - c0
    spectra = window[rr, cc, :]
    val = r[mask]

    # export
    df = pd.DataFrame({
        'idx': val,
        'fid': fid,})
    df_rfl = pd.DataFrame(spectra, columns=wvl_col_neon)
    df = pd.concat([df, df_rfl], axis=1)
    out.append(df)

out_table = pd.concat(out)
out_table = out_table.merge(gdf[['target', 'idx']], on='idx', how='left')
fp_out = 'validation/rfl_insitu_neon_hrdf.csv'
out_table.to_csv(fp_out, index=False)