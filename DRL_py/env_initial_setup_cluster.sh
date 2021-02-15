#!/bin/bash -l

dir_base=${PWD}/env/DRL_base_case

mkdir -p $dir_base

cp -r ${PWD}/env/base_case/* $dir_base

sed -i "/^startTime/ s/startTime.*/startTime       0;/g" $dir_base/system/controlDict
sed -i "/^endTime/ s/endTime.*/endTime         $1;/g" $dir_base/system/controlDict

sentence=$(sbatch env_hpc_initial.sh)              # get the output from sbatch

stringarray=($sentence)                            # separate the output in words
jobid=(${stringarray[3]})                          # isolate the job ID
sentence="$(squeue -j $jobid)"       		   # read job's slurm status
stringarray=($sentence) 
jobstatus=(${stringarray[12]})            	   # isolate the status of job number jobid

while [ "$jobstatus" = "R" ] || [ "$jobstatus" = "PD" ];
do
  echo "waiting for initial setup.."
  sentence="$(squeue -j $jobid)"                     # read job's slurm status
  stringarray=($sentence)
  jobstatus=(${stringarray[12]})                     # isolate the status of job number jobid
  sleep 03
done

