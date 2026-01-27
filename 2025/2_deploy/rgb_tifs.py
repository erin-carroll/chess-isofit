import rasterio
from glob import glob
import os
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2025/deploy_6c_20260120/')

fp = '/store/carroll/repos/chess-isofit/2025/2_deploy/insitu_validation_fids_2025.txt'
fids = [x.strip() for x in open(fp).readlines()]

fps = [x for x in glob('*/output/*rfl') if 'subs' not in x]
fps = [x for x in fps if any(fid in x for fid in fids)]

for fp in tqdm(fps):
    out_fp = f'rgb_tifs/{os.path.basename(fp).replace("rfl", "rfl_rgb.tif")}'
    if os.path.exists(out_fp):
        continue
    with rasterio.open(fp) as src:
        profile = src.profile
        profile.update(
            driver='GTiff',
            count=3,
            compress='lzw',
            tiled=True,
            blockxsize=256,
            blockysize=256,
            interleave='pixel'
        )

        
        r = src.read(60)
        g = src.read(40)
        b = src.read(30)

        rgb = rasterio.open(
            out_fp,
            'w',
            **profile
        )
        rgb.write(r, 1)
        rgb.write(g, 2)
        rgb.write(b, 3)
        rgb.close()