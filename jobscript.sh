#!/bin/bash
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=cylinder_
#SBATCH --ntasks-per-node=2

module load singularity/3.6.0rc2
module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

mpirun -np 2 singularity run of2006-py1.6-cpu.sif ./Allrun ./test_cases/run/singularity_test/

singularity run of2006-py1.6-cpu.sif ./Allrun ./test_cases/run/singularity_test/
