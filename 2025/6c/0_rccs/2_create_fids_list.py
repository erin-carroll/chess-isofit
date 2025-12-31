import os
from glob import glob

fids = glob('/store/carroll/col/data/2025/rccs/subsets/*_rdn.hdr')
fids = list(set([x.split('/')[-1].split('_rdn')[0] for x in fids]))

fp_out = '/store/carroll/repos/chess-isofit/2025/3c/0_rccs/rccs_2025_fids.txt'
with open(fp_out, 'w') as f:
    f.write('\n'.join(fids))