import rasterio
from glob import glob
import os
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2018/deploy_6c_20260120/')

fids = ['NIS01_20180619_154149',
        'NIS01_20180619_155226',
        'NIS01_20180619_160339',
        'NIS01_20180619_161406',
        'NIS01_20180613_170023',
        'NIS01_20180613_171044',
        'NIS01_20180613_172129',
        'NIS01_20180625_165243',
        'NIS01_20180625_170354']

fps = [x for x in glob('*/output/*rfl') if 'subs' not in x]
fps = [x for x in fps if any(fid in x for fid in fids)]
print(len(fps))

for fp in tqdm(fps):
    out_fp = f'rgb_tifs/{os.path.basename(fp).replace("rfl", "rfl_rgb_150-250-350.tif")}'
    if os.path.exists(out_fp):
        continue
    print(out_fp)

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

       
        r = src.read(150)
        g = src.read(250)
        b = src.read(350)

        rgb = rasterio.open(
            out_fp,
            'w',
            **profile
        )
        rgb.write(r, 1)
        rgb.write(g, 2)
        rgb.write(b, 3)
        rgb.close()