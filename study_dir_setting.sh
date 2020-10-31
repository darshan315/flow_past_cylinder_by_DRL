#!/bin/bash

# maketh of all folders
frequency=($(seq 1 1 2))
amplitude=($(seq 1 1 2))

FOLDERS=test_cases/run/oscillatory_parameter_study/cases

for i in "${amplitude[@]}"
do
	for j in "${frequency[@]}"
	do	
		mkdir -p $FOLDERS/A$i-f$j
		cp -r test_cases/run/oscillatory_parameter_study/base_pre-mesh/* $FOLDERS/A$i-f$j/
	
		cd ./$FOLDERS/A$i-f$j/
		echo -e "\nAmplitude = $i  frequency = $j \n"
		./change_param ch_amp $i
		./change_param ch_fq $j
		# delete file of base_mesh (unrequired for rest of computation)
		rm prepare_base_mesh.sh
		rm run_base_mesh
		
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

singularity run of2006-py1.6-cpu.sif ./pre_processing ./$FOLDERS/A$i-f$j/
mpirun -np 2 singularity run of2006-py1.6-cpu.sif ./sim_processing ./$FOLDERS/A$i-f$j/
EOF
	chmod +x jobscript.sh
#----------------------------------------------------------------------------#	
		
		cd .. ; cd .. ; cd .. ; cd .. ; cd ..	
	done
done
