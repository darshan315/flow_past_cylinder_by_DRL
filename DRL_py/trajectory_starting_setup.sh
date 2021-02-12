#!/bin/bash


# here simulation will be run till 6 second and random value bewtween 4-6 will be taken by uniform sampling to start simulation by startTime = $random value

# random value will be set to nearest dalta_T of simulation. e.g. if time is [0, 0.3, 0.6, ...] and random value is 0.2 then this will be set to 0.3

# end time will be set to endTime = $startTime + t : for uniform length of trajectory
dirs=${PWD}/env/trajectories/trajectory_$1_$2

mkdir -p $dirs

cp -r ${PWD}/env/DRL_base_case/* $dirs

sed -i "1,/startTime/ s/startTime.*/startTime       0;/g" $dirs/system/controlDict
sed -i "1,/endTime/ s/endTime.*/endTime       $2;/g" $dirs/system/controlDict
sed -i "0,/frequency/ s/frequency.*/frequency        0;/g" $dirs/0/U

cd ${PWD}/env/trajectories/trajectory_$1_$2

#----------------------------------------------------------------------------#		
# creates jobscript in each folder	
cat > jobscript.sh <<EOF
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=A$i-f$j
#SBATCH --ntasks-per-node=2

module load singularity/3.6.0rc2
module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

singularity run of2006-py1.6-cpu.sif ./pre_processing ./$dirs/
mpirun -np 2 singularity run of2006-py1.6-cpu.sif ./sim_processing ./$dirs/

echo "done_$1_$2" >> done.txt

EOF
	chmod +x jobscript.sh
#----------------------------------------------------------------------------#	

cd ../../..
