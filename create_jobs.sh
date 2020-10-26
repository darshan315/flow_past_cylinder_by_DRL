#!/bin/bash

for folder in $(ls -d test_cases/run/oscillatory_parameter_study/*); do
  
cat > $folder/jobscript.sh <<EOF
#!/bin/bash
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=cylinder_
#SBATCH --ntasks-per-node=2

module load singularity/3.6.0rc2

singularity run of2006-py1.6-cpu.sif ./Allrun $folder
EOF
 	
	chmod +x $folder/jobscript.sh
 	
done
