import os
from glob import glob

raw = '/store/carroll/col/data/2025/mosaic/cloud_shadow_masks/'
out_fol = '/store/carroll/col/data/2025/mosaic/file_lists/'
fps = [x.removesuffix('.hdr') for x in sorted(glob(os.path.join(raw, '*.hdr')))]
print(len(fps))
print(fps[0:5])

for domain in ['ALMO', 'CRBU', 'UPTA']:
    domain_fids = [x for x in fps if domain in x]
    print(domain, len(domain_fids))
    print(domain_fids)
    with open(os.path.join(out_fol, f'cloud_shadow_{domain}.txt'), 'w') as f:
        for fid in domain_fids:
            f.write(f'{fid}\n')