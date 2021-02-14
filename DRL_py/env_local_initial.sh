#!/bin/bash

dir_base=${PWD}/env/DRL_base_case

mkdir -p $dir_base

cp -r ${PWD}/env/base_case/* $dir_base

sed -i "/^startTime/ s/startTime.*/startTime       0;/g" $dir_base/system/controlDict
sed -i "/^endTime/ s/endTime.*/endTime         $1;/g" $dir_base/system/controlDict

singularity run of2006-py1.6-cpu.sif ./Allrun ./env/DRL_base_case/
