#!/bin/bash -l        
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=init_set
#SBATCH --ntasks-per-node=4

module load singularity/3.6.0rc2

singularity run of2006-py1.6-cpu.sif ./Allrun ./env/DRL_base_case/
