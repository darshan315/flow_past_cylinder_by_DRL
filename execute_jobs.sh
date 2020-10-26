#!/bin/bash
for folder in $(ls -d test_cases/run/oscillatory_parameter_study/*); do
  sbatch $folder/jobscript.sh
done
