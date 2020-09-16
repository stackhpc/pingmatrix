Run an MPI job (e.g. IMB PingPong) on all pairs of nodes in a Slurm cluster.

# Usage:

1. Modify a template script to suit your need, e.g. see`ping-ib.tpl`:
    - The following keys are provided for `{interpolation}`:
        - `template_file`: the name of the template file, excluding any directory components
        - `exclude_nodes`: should be used to create an `#SBATCH --exclude=` directive to control which nodes are used
    - It should extract the variable(s) to measure in some grep-able format - this uses `readping.py` to extract zero-size message latency and maximum bandwidth.

1. Run

        python runping.py <template_path>

    This will launch a job for each pair of nodes.

1. Use something like:

        watch "squeue -h -u $USER | wc -l"

    To monitor how many jobs are left in the queue.

1. Grep for your results marker.
