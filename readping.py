""" Read IMB output.

    Usage:
        python imb.py <stdout_file>
"""

# examples of output - note that a single file *may* contain multiple
# benchmark results
#
# # Benchmarking Uniband 
# # #processes = 2 
# #---------------------------------------------------
#        #bytes #repetitions   Mbytes/sec      Msg/sec
#             0         1000         0.00      2189915
#
# # Benchmarking PingPong 
# # #processes = 2 
# #---------------------------------------------------
#        #bytes #repetitions      t[usec]   Mbytes/sec
#             0         1000         2.25         0.00

def summarise_ping(path):
    datas = read_imb_out(path)
    if len(datas) > 1:
        raise ValueError('Cannot summarise file with multiple tables: %s' % path)
    n_procs = list(datas.keys())
    first_data = datas[n_procs[0]]
    zero_latency = first_data['t[usec]'][0]
    max_bw = max(first_data['Mbytes/sec'])
    print('%s us' % zero_latency, '%s MB/s' % max_bw)
    
def read_imb_out(path):
    """ Read stdout from an IMB-MPI1 run.
        
        Returns a dict with:
            key:= int, total number of processes involved
            value:= dict, keys are table columns
        
        If multiple results tables are present it is assumed that they are all the same benchmark,
        and only differ in the number of processes.
    """

    dframes = {}

    COLTYPES = { # all benchmark names here should be lowercase
        'uniband': (int, int, float, int), # #bytes #repetitions Mbytes/sec Msg/sec
        'biband': (int, int, float, int),
        'pingpong':(int, int, float, float), # #bytes #repetitions t[usec] Mbytes/sec
        'alltoall':(int, int, float, float, float) # #bytes #repetitions t_min[usec] t_max[usec] t_avg[usec]
    }
    
    with open(path) as f:
        for line in f:
            if line.startswith('# Benchmarking '):
                benchmark = line.split()[-1].lower()
                if benchmark not in COLTYPES:
                    raise ValueError('Do not know how to read %r benchmark in %s' % (benchmark, path))
                converters = COLTYPES[benchmark]
                line = next(f)
                expect = '# #processes = '
                if not line.startswith(expect):
                    raise ValueError('expected %s, got %s' % (expect, nprocs_line))
                n_procs = int(line.split('=')[-1].strip())
                while line.startswith('#'):
                    line = next(f) # may or may not include line "# .. additional processes waiting in MPI_Barrier", plus other # lines
                colnames = line.strip().split()
                data = dict((c, []) for c in colnames)
                while True:
                    parts = next(f).strip().split()
                    if not parts:
                        break
                    values = [f(v) for (f, v) in zip(converters, parts)]
                    for ix, k in enumerate(data): # depends on dicts being insertion order in py3
                        data[k].append(converters[ix](parts[ix]))
                    
                dframes[n_procs] = data
    return dframes

if __name__ == '__main__':
    import sys
    summarise_ping(sys.argv[1])
