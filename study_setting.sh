#!/bin/bash

# copy from base to run as mesh_base_case
mkdir -p test_cases/run/base_pre-mesh
cp -r test_cases/oscillatory_boundary_condition test_cases/run/oscillatory_parameter_study/base_pre-mesh/

if [ $1 == 'mesh' ] || [ $2 == 'mesh' ]
	cd test_cases/run/base_pre-mesh/
	run mesh
	blockMesh &> log.blockMesh
	snappyHexMesh -overwrite  &> log.snappyHexMesh
	extrudeMesh &> log.extrudeMesh
	cd .. ; cd .. ; cd .. ;
fi


# maketh of all folders
fq=($(seq 1 1 10))
amp=($(seq 1 1 10))

if [ $1 == 'dirs' ] || [ $2 == 'dirs' ]
	for i in "${amplitude[@]}"
	do
		for j in "${frequency[@]}"
		do	
			mkdir -p test_cases/run/oscillatory_parameter_study/A_$i-f_$j
			cp -r test_cases/run/oscillatory_parameter_study/base_pre-mesh/* test_cases/run/oscillatory_parameter_study/A_$i-f_$j/
		
			cd ./test_cases/run/oscillatory_parameter_study/A_$i-f_$j/
			echo -e "\nAmplitude = $i  frequency = $j \n"
			./change_param ch_amp $i
			./change_param ch_fq $j
			cd .. ; cd .. ; cd .. ; cd ..	
		done
	done			 		
fi

