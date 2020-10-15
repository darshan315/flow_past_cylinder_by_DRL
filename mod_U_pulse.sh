#!/usr/bin/bash

declare -a amplitude
amplitude=( 1.00 2.00 4.00 )
	
for i in "${amplitude[@]}"
do
	cp -r v1_test_case/cylinder2D_base v1_test_case/run/amplitude_$i
	mkdir -p notebooks/oscillatory_bounday_condition/cases_amplitude/amplitude_$i
	cd ./v1_test_case/run/amplitude_$i/
	echo -e "******************************************************************"
	echo -e "\nAmplitude = $i\n"
	echo -e "******************************************************************"
	./Allclean
	./change_param ch_amp $i
	./Allrun
	touch done.txt
	cd .. ; cd .. ; cd ..
	cp -r v1_test_case/run/amplitude_$i/system notebooks/oscillatory_bounday_condition/cases_amplitude/amplitude_$i
	cp -r v1_test_case/run/amplitude_$i/postProcessing notebooks/oscillatory_bounday_condition/cases_amplitude/amplitude_$i
	
done
