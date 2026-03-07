import os
import pandas as pd
from glob import glob

for year in [2018, 2025]:
    fps = glob(f'/store/carroll/col/data/extractions/csv/*{year}*_extraction.csv')
    print(year, len(fps))
    if len(fps)>0:
        dfs = [pd.read_csv(fp) for fp in fps]
        df = pd.concat(dfs, ignore_index=True)
        print(df.shape)
        fp_out = f'/store/carroll/col/data/extractions/site_extraction_spectra_{year}.csv'
        df.to_csv(fp_out, index=False)