#!/bin/bash

for folder in $(ls -d test_cases/run/lhs/cases/*); do
  mkdir -p ${PWD}/notebooks/oscillatory_bounday_condition/lhs_data/$(basename $folder A)
  ln -s ${PWD}/$folder/postProcessing/forces/0/coefficient.dat ${PWD}/notebooks/oscillatory_bounday_condition/lhs_data/$(basename $folder A)/coefficient.dat
done

