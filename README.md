Run and process an sbatch job on all pairs of nodes in a Slurm cluster.

# Usage:

1. Create an sbatch script template - see `ping-ib.tpl` for an example. It MUST contain:

    #SBATCH --exclude={exclude_nodes}
    #SBATCH --output={output}
    #SBATCH --error={error}

    It may also include `{template_file}` to record the template file name in the generated files.
    
1. Run

        ./matrix run <template_path>

    where `<template_path>` is the template created above.

    e.g.:

        ./matrix run ping-ib.tpl

    This will create an sbatch script and submit it for each pair of nodes. It will also create a `.nodemap` file needed for postprocessing.

1. Use something like:

        watch "squeue -h -u $USER | wc -l"

    To monitor how many jobs are left in the queue.

1. Once finished, run:

        ./matrix read <template_path> <postprocess> [<postprocess_args_and_options> ...]

    where `<template_path>` is as above and `<postprocess>` is the path to an executable to process run output.

    examples:

        ./matrix.py read ping-ib.tpl ./imb-stats.py # reports IMB pingpong zero-size message latency
        ./matrix.py read ping-ib.tpl ./imb-stats.py # reports IMB pingpong maximum bandwidth
        ./matrix.py read <template> grep <somepattern>

    The `<postprocess>` executable must:
    - Take the path to a file containing stdout from an `sbatch` script as its last argument.
    - Output a result to stdout.
    
    A comma-separated matrix of results will be output.

    **NB** sorting of nodenames in that matrix assumes they contain integer components.