#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=cy_osc
#SBATCH --ntasks-per-node=4

module load singularity/3.6.0rc2
module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

singularity run of2006-py1.6-cpu.sif ./pre_processing ./test_cases/run/oscillatory_boundary_condition/
mpirun -np 4 singularity run of2006-py1.6-cpu.sif ./sim_processing ./test_cases/run/oscillatory_boundary_condition/
