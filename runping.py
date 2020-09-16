""" Run using e.g.:

    python runping.py ping-roce.tpl
"""

__version__ = '0.1'

import itertools, sys, os, subprocess, re

def get_hostnames():
    """ Query slurm for a list of hostnames """
    hostlist = subprocess.run(['sinfo', '-h', '--format', '%N'], capture_output=True, text=True).stdout.strip()
    hostnames = subprocess.run(['scontrol', 'show', 'hostnames', hostlist], capture_output=True, text=True).stdout.split()
    return hostnames

def get_hostlist(hostnames):
    hostlist = subprocess.run(['scontrol', 'show', 'hostlist', hostnames], capture_output=True, text=True).stdout.strip()
    return hostlist

if __name__ == '__main__':

    template_file = sys.argv[1]
    template_name = os.path.splitext(template_file)[0]

    hostnames = get_hostnames() # TODO: select specific partitions?
    
    nodecombos = list(itertools.combinations(hostnames, 2))
    
    with open(template_file) as f:
        template = f.read()

    for runid, (node_a, node_b) in enumerate(nodecombos):
        exclude_nodes = ','.join(sorted(set(hostnames) - set((node_a, node_b))))
        rendered = template.format(template_file=template_file, exclude_nodes=exclude_nodes)
        
        sbatch_name = '%s-%s.sh' % (template_name, runid)
        with open(sbatch_name, 'w') as scriptf:
            scriptf.write(rendered)
        os.system('sbatch %s' % sbatch_name)
