#!/bin/bash -l        

dir_base=${PWD}/env/trajectories

mkdir -p $dir_base/trajectory_$1

cp -r ${PWD}/env/DRL_base_case/* $dir_base/trajectory_$1

sed -i "/^startFrom/ s/startFrom.*/startFrom       latestTime;/g" $dir_base/trajectory_$1/system/controlDict
sed -i "/^endTime/ s/endTime.*/endTime         $2;/g" $dir_base/trajectory_$1/system/controlDict

rm $dir_base/trajectory_$1/log.blockMesh
rm $dir_base/trajectory_$1/log.snappyHexMesh
rm $dir_base/trajectory_$1/log.extrudeMesh
rm $dir_base/trajectory_$1/log.setExprBoundaryFields
rm $dir_base/trajectory_$1/log.pimpleFoam


# file 2
cat > $dir_base/trajectory_$1/job_traj_$1.sh <<EOF
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=traj_$1
#SBATCH --ntasks-per-node=2

module load singularity/3.6.0rc2

singularity run of2006-py1.6-cpu.sif ./sim_processing ./env/trajectories/trajectory_$1/

EOF

chmod +x $dir_base/trajectory_$1/job_traj_$1.sh

sentence=$(sbatch env/trajectories/trajectory_$1/job_traj_$1.sh) # get the output from sbatch
stringarray=($sentence)                            # separate the output in words
jobid=(${stringarray[3]})                          # isolate the job ID
sentence="$(squeue -j $jobid)"       		   # read job's slurm status
stringarray=($sentence) 
jobstatus=(${stringarray[12]})            	   # isolate the status of job number jobid

while [ "$jobstatus" = "R" ] || [ "$jobstatus" = "PD" ];
do
  echo "waiting for trajectory_$1.."
  sentence="$(squeue -j $jobid)"                     # read job's slurm status
  stringarray=($sentence)
  jobstatus=(${stringarray[12]})                     # isolate the status of job number jobid
  sleep 03
done
