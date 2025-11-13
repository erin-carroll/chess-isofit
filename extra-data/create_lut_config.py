import json

version = '20251001'
fp_out = f'/store/carroll/col/data/2018/extra_data/lut_config_{version}.json'

config = {}
config['h2o_range'] = [0.0001,3]

with open(fp_out, 'w') as f:
    json.dump(config, f)