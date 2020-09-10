#!/bin/bash
# produced from {template_file}
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
#SBATCH --time=0:10:0
#SBATCH --exclusive
#SBATCH --exclude={exclude_nodes}
#SBATCH --job-name={job_prefix}
#SBATCH --output={job_prefix}.out
#SBATCH --error={job_prefix}.err

echo "running on nodes {node_a} {node_b}"
module load gcc/9.3.0-5abm3xg
module load openmpi/4.0.3-qpsxmnc
export SLURM_MPI_TYPE=pmix_v2
export UCX_NET_DEVICES=mlx5_1:1
module load intel-mpi-benchmarks/2019.5-dwg5q6j
srun IMB-MPI1 pingpong
