#!/bin/bash -l        
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=7-00:00:00
#SBATCH --job-name=py_drl
#SBATCH --ntasks-per-node=1

source ~/venv/bin/activate 

python3 main.py &> py.log
