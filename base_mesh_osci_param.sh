#!/bin/bash

mkdir -p test_cases/run/oscillatory_parameter_study/base_pre-mesh

cp -r test_cases/oscillatory_boundary_condition/* test_cases/run/oscillatory_parameter_study/base_pre-mesh/

# file 1
cat > test_cases/run/oscillatory_parameter_study/base_pre-mesh/run_base_mesh <<EOF
#!/bin/bash -l
blockMesh &> log.blockMesh
snappyHexMesh -overwrite  &> log.snappyHexMesh
extrudeMesh &> log.extrudeMesh
cp -r 0.org 0

EOF


# file 2
cat > test_cases/run/oscillatory_parameter_study/base_pre-mesh/prepare_base_mesh.sh <<EOF
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=CY_MESH
#SBATCH --ntasks-per-node=2

module load singularity/3.6.0rc2

singularity run of2006-py1.6-cpu.sif ./run_base_mesh ./test_cases/run/oscillatory_parameter_study/base_pre-mesh

EOF

chmod +x test_cases/run/oscillatory_parameter_study/base_pre-mesh/run_base_mesh
chmod +x test_cases/run/oscillatory_parameter_study/base_pre-mesh/prepare_base_mesh.sh

sbatch test_cases/run/oscillatory_parameter_study/base_pre-mesh/prepare_base_mesh.sh
