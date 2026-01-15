import os
from glob import glob
import numpy
from spectral.io import envi

os.chdir('/store/carroll/col/data/2018/deploy_3c_20251126')

fids = glob('NIS01*')
print(len(fids))

for fid in fids:
    fp = os.path.join(fid, 'output', f'{fid}_atm_interp.hdr')
    arr = envi.open(fp).open_memmap()[..., 0]
    arr = arr[arr!=-9999]
    print(fid, numpy.nanmin(arr), numpy.nanmax(arr))
