import os
from glob import glob
import numpy as np
from spectral.io import envi

os.chdir('/store/carroll/col/data/2025/')

fids = [
    'CRBU_DP1_L064-1_20250702',
    'ALMO_DP1_L046-1_20250613',
    'ALMO_DP1_L043-2_20250614',
    'ALMO_DP1_L058-1_20250614'
    ]

for fid in fids:
    print(fid)
    fps = glob(f'/store/carroll/col/data/2025/raw/L1/radianceENVI/NEON_D13_{fid}_rdn_*.hdr')
    print(len(fps))

    arrs = [envi.open(fp) for fp in fps]

    total_bands = sum(x.shape[-1] for x in arrs)
    print('total bands:', total_bands)

    # build metadata
    base_md = dict(arrs[0].metadata)
    md = dict(base_md)
    md["bands"] = str(total_bands)

    fp_out = f'/store/carroll/col/data/2025/raw/L1/radianceENVI/NEON_D13_{fid}_rdn.hdr'
    out_img = envi.create_image(fp_out, md, ext="", force=True)
    out_mm = out_img.open_memmap(writable=True)

    # Copy data in chunks
    out_band0 = 0
    for in_hdr, im in zip(fps, arrs):
        in_mm = im.open_memmap()  # read-only memmap
        nb = im.shape[-1]
        print(f"Copying {os.path.basename(in_hdr)}: {nb} bands -> out bands [{out_band0}:{out_band0+nb}]")

        out_mm[..., out_band0:out_band0+nb] = in_mm
        out_band0 += nb

    # Flush to disk
    out_mm.flush()
    print(f"Done. Wrote {total_bands} bands -> {fp_out}")
