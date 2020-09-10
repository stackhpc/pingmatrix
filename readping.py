""" Run using e.g.:

    python readping.py *roce*.out
"""

import sys, glob, os

results = {} # key: (a, b) value->latency

files = sys.argv[1:]
for path in files:
    name = os.path.splitext(path)[0]
    a, b = name.rsplit('-', 3)[2:]
    a = int(a)
    b = int(b)
    with open(path) as f:
        for line in f:
            if line.startswith('       #bytes #repetitions      t[usec]   Mbytes/sec'):
                zero_size = next(f).strip()
                bytes, reps, latency, bw = zero_size.split()
                results[(a, b)] = latency

# get sorted list of all options:
ids = []
for k in results.keys():
    ids.extend(k)
ids = sorted(set(ids))
header = ['    '] + ['{:4}'.format(v) for v in ids]
print(','.join(header))
for a in ids:
    rowvals = ['{:4}'.format(a)]
    for b in ids:
        lat = '{:4}'.format(results.get((a, b), '-'))
        rowvals.append(lat)
    print(','.join(rowvals))
