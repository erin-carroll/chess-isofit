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

os.chdir('/store/carroll/col/data')

wl_neon = np.loadtxt('/store/carroll/col/data/wavelengths_neon.txt')[:,1]*1000 # nm
wvl_col_neon = [f'w{x}' for x in wl_neon]

gdf = gpd.read_file('2025/validation/pseudoinvariant_sites_fids.geojson')
gdf['idx'] = gdf.index
fids = gdf.flightline.unique()

# extract isofit 6c rfl 2018, 2025
out = []
for fid in tqdm(fids):

    tmp = gdf[gdf['flightline']==fid] # filter raster_plot_event to a single fid

    # rasterize filtered gdf
    try:
        if '2018' in fid:
            fp = glob(os.path.join('2018/deploy_6c_20260214', f'{fid}', 'output', f'{fid}_rfl'))[0]
        if '2025' in fid:
            date = fid.split('_')[-2]
            line = fid.split('_')[-3]
            fp = glob(os.path.join('2025/deploy_6c_2014', f'*{date}*{line}', 'output', '*_rfl'))[0]
    except:
        print(f'No file found for {fid}')
        continue
        
    line_id = fp.split('/')[1].split('_')[-1]
    gdf.loc[gdf['flightline']==fid, 'line_id'] = line_id
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
out_table = out_table.merge(gdf[['site', 'idx']], on='idx', how='left')
fp_out = '2025/validation/rfl_pseudoinvariant_deploy6c20260214.csv'
out_table.to_csv(fp_out, index=False)