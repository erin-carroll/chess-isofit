import os
from glob import glob

os.chdir('/store/carroll/col/data/2025/raw/L1/radianceENVI/')

fs = glob('NIS01_20250628*CRBU*L036*')
print(len(fs), 'files found')