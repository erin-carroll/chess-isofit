import rasterio

fp_in = '/store/carroll/col/data/2018/deploy_3c_20251001/NIS01_20180625_164400/output/NIS01_20180625_164400_rfl'
fp_out = '/store/carroll/col/data/2018/test_flightlines/NIS01_20180625_164400_rfl_rgb.tif'

rgb_bands = [60,40,30]

with rasterio.open(fp_in) as src:
    profile = src.profile.copy()

    profile.update(
        driver="GTiff",
        count=len(rgb_bands),
        compress="deflate",   # or "lzw"
        predictor=2,          # good for continuous data
        tiled=True,
        blockxsize=256,
        blockysize=256,
        bigtiff="if_safer",
        interleave="band"
    )

    with rasterio.open(fp_out, "w", **profile) as dst:
        for i, b in enumerate(rgb_bands, start=1):
            data = src.read(b)   # read a single band (1-based index)
            dst.write(data, i)