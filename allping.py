""" Run using e.g.:

    python allping.py ping-roce.tpl
"""

import itertools, sys, os

template_file = sys.argv[1]
template_name = os.path.splitext(template_file)[0]

hostpattern = 'openhpc-compute-%i'
suffixes = range(0, 16)
combos = list(itertools.combinations(suffixes, 2))

with open(template_file) as f:
    template = f.read()

for a, b in combos:
    exclude_sx = sorted(set(suffixes) - set((a, b)))
    exclude_nodes = ','.join([hostpattern % i for i in exclude_sx])
    node_a = hostpattern % a
    node_b = hostpattern % b
    job_prefix = '{template_name}-{a}-{b}'.format(template_name=template_name, a=a, b=b)
    rendered = template.format(template_file=template_file, a=a, b=b, node_a=node_a, node_b=node_b, exclude_nodes=exclude_nodes, job_prefix=job_prefix)
    sbatch_name = '%s-%s-%s.sh' % (template_name, a, b)
    with open(sbatch_name, 'w') as scriptf:
        scriptf.write(rendered)
    os.system('sbatch %s' % sbatch_name)
