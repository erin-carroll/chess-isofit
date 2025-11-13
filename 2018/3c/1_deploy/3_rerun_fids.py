from glob import glob
import os
import re

fp_fids = '/store/carroll/repos/chess-isofit/2018/3c/1_deploy/crbu_2018_fids.txt'
with open(fp_fids, 'r') as f:
    fids = f.read().split('\n')

finished = []
failed = []
never_ran = []

for fid in fids:
    fp_logs = glob(f'/home/carroll/logs/*_all_flightlines_1c_20251001_{fid}.err')
    if len(fp_logs)==0:
        never_ran.append(fid)
    else:
        for fp in fp_logs:
            with open(fp, 'r', encoding='utf-8') as f:
                d = f.read()
                if 'Done.' in d:
                    finished.append(fid)
                else:
                    failed.append(fp)

failed_fids = list(set([x.split('20251001_')[-1].removesuffix('.err') for x in failed]))
failed_fids = [x for x in failed_fids if x not in finished]
rerun = failed_fids + never_ran

fp_out = '/store/carroll/repos/chess-isofit/2018/3c/1_deploy/crbu_2018_fids_failed_20251001.txt'
with open(fp_out, 'w') as f:
    f.write('\n'.join(rerun))