#!/usr/bin/usr
cp -r 0.org 0
runApplication setExprBoundaryFields
runApplication decomposePar
runParallel renumberMesh -overwrite
runParallel $(getApplication)

