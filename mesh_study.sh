#!/bin/bash

declare -a mesh_size
mesh_size=( 100 200 400 )
	
for i in "${mesh_size[@]}"
do
	mkdir -p test_cases/run/refinement_$i
	cp -r test_cases/cylinder2D_base test_cases/run/refinement_$i
	mkdir -p notebooks/plot_data/cases/case_$i
	cd ./test_cases/run/refinement_$i/cylinder2D_base/
	echo -e "******************************************************************"
	echo -e "\nMesh size = $i\n"
	echo -e "******************************************************************"
	./Allclean
	./mesh bmcell $i
	./solveronly
	cd .. ; cd .. ; cd ..; cd ..
	cp -r test_cases/run/refinement_$i/cylinder2D_base/system notebooks/plot_data/cases/case_$i
	cp -r test_cases/run/refinement_$i/cylinder2D_base/postProcessing notebooks/plot_data/cases/case_$i
	
done
