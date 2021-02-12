#!/bin/bash

dirs=${PWD}/env/trajectories/trajectory_$1_$2

sed -i "1,/startTime/ s/startTime.*/startTime       latestTime;/g" $dirs/system/controlDict
sed -i '1,/endTime/ s/endTime.*/endTime       $startTime+0.04;/g' $dirs/system/controlDict
sed -i "0,/frequency/ s/frequency.*/frequency        $3;/g" $dirs/0/U

if [ -e $dirs/done.txt ]
then 
    rm $dirs/done.txt
fi 
