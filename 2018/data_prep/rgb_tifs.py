import rasterio
from glob import glob
import os
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2018/deploy_6c_20260120/')

fps = [x for x in glob('*/output/*rfl') if 'subs' not in x]
print(len(fps))

for fp in tqdm(fps):
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

        out_fp = f'rgb_tifs/{os.path.basename(fp).replace("rfl", "rfl_rgb.tif")}'
        print(out_fp)
        
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