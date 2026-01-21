import os
from glob import glob
import numpy as np

os.chdir('/store/carroll/col/data/2025/raw/L1/')

fids_any = glob('radianceENVI/*')
fids_any = list(set(['_'.join(x.split('_')[0:4]).split('/')[-1] for x in fids_any]))
print(len(fids_any))
# print(fids_any[:5])

# lis_almo = np.loadtxt('/store/carroll/repos/chess-isofit/2025/6c/1_deploy/ALMO_2025_fids.txt', dtype=str)
# lis_crbu = np.loadtxt('/store/carroll/repos/chess-isofit/2025/6c/1_deploy/CRBU_2025_fids.txt', dtype=str)
# lis_upta = np.loadtxt('/store/carroll/repos/chess-isofit/2025/6c/1_deploy/UPTA_2025_fids.txt', dtype=str)
# lis = lis_almo.tolist() + lis_crbu.tolist() + lis_upta.tolist()
# print(len(lis))

# fids_missing = [x for x in fids_any if x not in lis]
# print(len(fids_missing))
# print(fids_missing)

fids_rdn = glob('radianceENVI/*_IGM_Data')
fids_rdn = ['_'.join(x.split('_')[0:4]).split('/')[-1] for x in fids_rdn]
print(len(fids_rdn))

fids_missing_rdn = [x for x in fids_any if x not in fids_rdn]
print(fids_missing_rdn)