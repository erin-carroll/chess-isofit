import rasterio
from glob import glob
import os
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2025/raw/L1/')

fps = glob('radianceENVI/*ALMO*_rdn')
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
        )

        out_fp = fp.replace('radianceENVI', 'rgb_tifs').replace('_rdn', '_rdn_rgb.tif')

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