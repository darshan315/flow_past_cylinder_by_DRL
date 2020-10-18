#!/usr/bin/bash

declare -a amplitude
amplitude=( 5.00 8.00 )
	
declare -a frequency
frequency=( 5.00 8.00 )

for i in "${amplitude[@]}"
do

	for j in "${frequency[@]}"
	do	
		cp -r test_cases/oscillatory_boundary_condition test_cases/run/oscillatory_parameter_study/A_$i-f_$j
		mkdir -p notebooks/oscillatory_bounday_condition/cases_A_and_f/A_$i-f_$j
		cd ./test_cases/run/oscillatory_parameter_study/A_$i-f_$j/
		echo -e "******************************************************************"
		echo -e "\nAmplitude = $i  frequency = $j \n"
		echo -e "******************************************************************"
		./Allclean
		./change_param ch_amp $i
		./change_param ch_fq $j
		./Allrun
		cd .. ; cd .. ; cd .. ; cd ..
		cp -r test_cases/run/oscillatory_parameter_study/A_$i-f_$j/system notebooks/oscillatory_bounday_condition/cases_A_and_f/A_$i-f_$j
		cp -r test_cases/run/oscillatory_parameter_study/A_$i-f_$j/postProcessing notebooks/oscillatory_bounday_condition/cases_A_and_f/A_$i-f_$j
		
	done

done
