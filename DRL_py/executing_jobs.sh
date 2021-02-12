#!/bin/bash
for folder in $(ls -d ${PWD}/env/trajectories/trajectory_$1_$2/*); do
  sbatch $folder/jobscript.sh
done
