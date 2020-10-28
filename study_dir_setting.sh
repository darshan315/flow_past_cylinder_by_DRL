#!/bin/bash

# maketh of all folders
frequency=($(seq 1 1 2))
amplitude=($(seq 1 1 2))

for i in "${amplitude[@]}"
do
	for j in "${frequency[@]}"
	do	
		mkdir -p test_cases/run/oscillatory_parameter_study/cases/A_$i-f_$j
		cp -r test_cases/run/oscillatory_parameter_study/base_pre-mesh/* test_cases/run/oscillatory_parameter_study/cases/A_$i-f_$j/
	
		cd ./test_cases/run/oscillatory_parameter_study/cases/A_$i-f_$j/
		echo -e "\nAmplitude = $i  frequency = $j \n"
		./change_param ch_amp $i
		./change_param ch_fq $j
		# delete file of base_mesh (unrequired for rest of computation)
		rm prepare_base_mesh.sh
		rm run_base_mesh
		cd .. ; cd .. ; cd .. ; cd .. ; cd ..	
	done
done			 		


# creates jobscript in each folder
for folder in $(ls -d test_cases/run/oscillatory_parameter_study/cases/*); do
  
cat > $folder/jobscript.sh <<EOF
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=cylinder_
#SBATCH --ntasks-per-node=2

module load singularity/3.6.0rc2
module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

singularity run of2006-py1.6-cpu.sif ./pre_processing ./$folder
mpirun -np 2 singularity run of2006-py1.6-cpu.sif ./sim_processing ./$folder

EOF
 	
	chmod +x $folder/jobscript.sh
 	
done

