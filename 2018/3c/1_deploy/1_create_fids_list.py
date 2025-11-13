import os
from glob import glob

fids = glob('/store/carroll/col/data/2018/raw/rmbl/L1/*.hdr')
fids = list(set([x.split('/')[-1].split('_rdn')[0] for x in fids]))

fp_out = '/store/carroll/repos/chess-isofit/2018/3c/1_deploy/crbu_2018_fids.txt'
with open(fp_out, 'w') as f:
    f.write('\n'.join(fids))