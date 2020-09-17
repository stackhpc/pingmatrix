#!/usr/bin/env python
""" Run and process an sbatch job on all pairs of nodes in a Slurm cluster.

    Usage:
        ./matrix.py run TEMPLATE
        ./matrix.py read TEMPLATE POSTPROCESS [POSTPROCESS_ARGS ...]
"""

__version__ = '0.0'

import itertools, sys, os, subprocess, re, json, pprint

def get_hostnames():
    """ Query slurm for a list of hostnames """
    hostlist = subprocess.run(['sinfo', '-h', '--format', '%N'], capture_output=True, text=True).stdout.strip()
    hostnames = subprocess.run(['scontrol', 'show', 'hostnames', hostlist], capture_output=True, text=True).stdout.split()
    return hostnames

def get_hostlist(hostnames):
    hostlist = subprocess.run(['scontrol', 'show', 'hostlist', hostnames], capture_output=True, text=True).stdout.strip()
    return hostlist

def int_parts(s):
    return [int(v) for v in re.findall(r'\d+', s)]

def run(template_file):
    template_name = os.path.splitext(template_file)[0]
    hostnames = get_hostnames() # TODO: select specific partitions?
    nodecombos = list(itertools.combinations(hostnames, 2))

    with open(template_file) as f:
        template = f.read()
    
    nodemap = {} # key->sbatch name, value->(node_a, node_b)
    for runid, (node_a, node_b) in enumerate(nodecombos):
        
        sbatch = '%s-%s.sh' % (template_name, runid)
        exclude_nodes = ','.join(sorted(set(hostnames) - set((node_a, node_b))))
        output = '%s-%s.out' % (template_name, runid)
        error = '%s-%s.err' % (template_name, runid)
        rendered = template.format(template_file=template_file, exclude_nodes=exclude_nodes, output=output, error=error)
        # TODO: could check/add exclude/output/error directives?
        
        nodemap[output] = (node_a, node_b)
        with open(sbatch, 'w') as scriptf:
            scriptf.write(rendered)
        os.system('sbatch %s' % sbatch)
        
    with open('%s.nodemap' % template_name, 'w') as mapf:
        json.dump(nodemap, mapf, indent=2)

def read(template_file, pp_args):
    
    results = {} # (node_a, node_b) -> result: all are strings

    # read the mapping file:
    template_name = os.path.splitext(template_file)[0]
    with open('%s.nodemap' % template_name) as mapf:
        nodemap = json.load(mapf)
    
    # read all out files:
    for out_file, (node_a, node_b) in nodemap.items():
        if not os.path.exists(out_file):
            pass
        else:
            result = subprocess.run(pp_args + [out_file], capture_output=True, text=True).stdout.strip()
            results[node_a, node_b] = result

    # find all nodes:
    nodes = []
    for v in nodemap.values():
        nodes.extend(v)
    nodes = sorted(set(nodes), key=int_parts) ## sorts by (any number of) integer parts of each nodename

    # turn results into a nice grid:
    header = ['    '] + ['{:4}'.format(n) for n in nodes]
    print(','.join(header))
    for a in nodes:
        rowvals = ['{:4}'.format(a)]
        for b in nodes:
            lat = '{:4}'.format(results.get((a, b), '-'))
            rowvals.append(lat)
        print(','.join(rowvals))

    #print(nodes)
    exit()

    pprint.pprint(results)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        exit('Incorrect arguments, see docstring')
    elif sys.argv[1] == 'run':
        run(sys.argv[2])
    elif sys.argv[1] == 'read':
        read(sys.argv[2], sys.argv[3:])
    else:
        exit('Incorrect arguments, see docstring')
