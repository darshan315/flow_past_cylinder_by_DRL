#!/bin/bash

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

singularity run of2006-py1.6-cpu.sif ./sim_processing $dir_base/trajectory_$1/
