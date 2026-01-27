import os
from glob import glob

domains = ['ALMO', 'CRBU', 'UPTA']

# all fids for line-level apply_oe
fol = '/store/carroll/col/data/2025/raw/L1/radianceENVI'
for domain in domains:
    fp_out = f'/store/carroll/repos/chess-isofit/2025/2_deploy/{domain}_2025_fids.txt'
    fids = glob(os.path.join(fol, f'*{domain}*rdn'))
    fids = [os.path.basename(x).removesuffix('_rdn') for x in fids]
    with open(fp_out, 'w') as f:
        for fid in fids:
            f.write(fid + '\n')

# mosaicking lists
for domain in domains:
    print(domain)

    fp = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_obs_{domain}.txt'
    with open(fp) as f:
        fids = f.readlines()
    fids = [os.path.basename(x.strip()).removesuffix('_OBS_Data') for x in fids]
    print(len(fids))

    # rfl
    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_rfl_{domain}.txt'
    working_dir = '/store/carroll/col/data/2025/deploy_6c_20260120'
    with open(fp_out, 'w') as f:
        for fid in fids:
            f.write(f'{working_dir}/{fid}/output/{fid}_rfl' + '\n')

    # unc
    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_unc_{domain}.txt'
    working_dir = '/store/carroll/col/data/2025/deploy_6c_20260120'
    with open(fp_out, 'w') as f:
        for fid in fids:
            f.write(f'{working_dir}/{fid}/output/{fid}_uncert' + '\n')

    # shade
    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_shade_{domain}.txt'
    working_dir = '/store/carroll/col/data/2025/shade'
    with open(fp_out, 'w') as f:
        for fid in fids:
            fid_ = fid.split('_DP1')[0]
            f.write(f'{working_dir}/{fid_}_shade.tif' + '\n')

    # ewt
    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_ewt_{domain}.txt'
    working_dir = '/store/carroll/col/data/2025/deploy_6c_20260120'
    with open(fp_out, 'w') as f:
        for fid in fids:
            f.write(f'{working_dir}/{fid}/output/{fid}_ewt' + '\n')
