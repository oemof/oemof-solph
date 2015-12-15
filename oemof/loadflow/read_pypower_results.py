import re
import pandas as pd

file = 'app_results.txt'
x = open(file, "rt").readlines()
bus_idx = [i for i, item in enumerate(x) if item.startswith('|     Bus Data')]
bra_idx = [i for i, item in enumerate(x) if item.startswith('|     Branch Data')]
start = bus_idx[0]+5
end = bra_idx[0]-4
bus_data = x[start:end]

bus_id = []
vmag = []
vang = []
gp = []
gq = []
lp = []
lq = []

def mf(item):
    try:
        return float(item)
    except:
        return None

for row in bus_data:
    bus_id.append(mf(row[0:5]))
    vmag.append(mf(row[5:12]))
    vang.append(mf(row[12:21]))
    gp.append(mf(row[21:31]))
    gq.append(mf(row[31:41]))
    lp.append(mf(row[41:51]))
    lq.append(mf(row[51:61]))

my_dict1 = {'bus_id': bus_id,
            'vmag': vmag,
            'vang':vang,
            'gp': gp,
            'gq': gq,
            'lp': lp,
            'lq': lq}

bus_pd = pd.DataFrame.from_dict(my_dict1)


# branch data
start = bra_idx[0]+5
end = len(x)-3
bra_data = x[start:end]

bra_id = []
f_bus = []
t_bus = []
fp = []
fq = []
tp = []
tq = []
lp = []
lq = []


for row in bra_data:
    bra_id.append(mf(row[0:4]))
    f_bus.append(mf(row[4:11]))
    t_bus.append(mf(row[11:18]))
    fp.append(mf(row[18:28]))
    fq.append(mf(row[28:38]))
    tp.append(mf(row[38:48]))
    tq.append(mf(row[48:58]))
    lp.append(mf(row[58:68]))
    lq.append(mf(row[68:78]))

my_dict2 = {'bra_id': bra_id,
            'f_bus': f_bus,
            't_bus': t_bus,
            'fp': fp,
            'fq': fq,
            'tp': tp,
            'tq': tq,
            'lp': lp,
            'lq': lq}

bra_pd = pd.DataFrame.from_dict(my_dict2)
