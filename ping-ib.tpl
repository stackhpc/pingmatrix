#!/bin/bash
# produced from {template_file}
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
#SBATCH --time=0:10:0
#SBATCH --exclusive
#SBATCH --exclude={exclude_nodes}
#SBATCH --output={output}
#SBATCH --error={error}

nodes=$(scontrol show hostnames $SLURM_JOB_NODELIST)
module load gcc/9.3.0-5abm3xg
module load openmpi/4.0.3-qpsxmnc
export SLURM_MPI_TYPE=pmix_v2
export UCX_NET_DEVICES=mlx5_0:1
module load intel-mpi-benchmarks/2019.5-dwg5q6j
srun IMB-MPI1 pingpong
