import os
from glob import glob

raw = '/store/carroll/col/data/2025/raw/L1/radianceENVI'
out_fol = '/store/carroll/repos/chess-isofit/2025/3c/1_deploy'
fids = sorted(glob(os.path.join(raw, '*_rdn')))
fids = [x.split('/')[-1] for x in fids]
fids = ['_'.join(x.split('_')[0:4]) for x in fids]
print(len(fids))
print(fids)

for domain in ['ALMO', 'CRBU', 'UPTA']:
    domain_fids = [x for x in fids if domain in x]
    print(domain, len(domain_fids))
    print(domain_fids)
    with open(os.path.join(out_fol, f'{domain}_2025_fids.txt'), 'w') as f:
        for fid in domain_fids:
            f.write(f'{fid}\n')