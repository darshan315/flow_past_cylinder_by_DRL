#!/bin/bash
LANG=en_US
: '
  lhs stands for Latin hypercube sampling.
  it is used to generate evenly distributed samples over multidimensional data space.
  :param n: number of sample
  :param a: lower bound of data space eg. [a,b] = [0,1]
  :param b: higher bound of data space eg. [a,b] = [0,1]
  :return:
  referance : https://youtu.be/r6rp-Qxc9xI
'

lhs(){
	dif=$(echo "scale=3; $(echo $2 - $1 | bc) / $n" | bc -l);
	l_lim=($(seq $1 $dif $(echo $2 - $dif | bc)))
	h_lim=($(seq $(echo $1 + $dif | bc) $dif $2))
	points=()
	for ((i=0;i<$n;i++)) ; do 
		di=${l_lim[i]}
		dj=${h_lim[i]}
		p=$(awk -v min=$di -v max=$dj -v seed=$RANDOM 'BEGIN{srand(seed); print  min+rand()*int(1000*(max-min)+1)/1000}')
		points+=("${p}")
	done
	shuf_points=( $(shuf -e "${points[@]}") )
	
}

n=10
a=(3 15)
b=(0.1 3.5)

lhs ${a[0]} ${a[1]}
frequency=("${shuf_points[@]}")

lhs ${b[0]} ${b[1]}
amplitude=("${shuf_points[@]}")

for ((i=0;i<$n;i++));do 
echo "${amplitude[i]},${frequency[i]}" >> data_LHS.csv
done

FOLDERS=test_cases/run/oscillatory_parameter_study/cases
mesh_dir=test_cases/run/oscillatory_parameter_study/base_pre-mesh

for ((t=0;t<$n;t++)) ; do
    i=${amplitude[t]}
    j=${frequency[t]}
	mkdir -p $FOLDERS/A$i-f$j
	ln -s ${PWD}/$mesh_dir/constant ${PWD}/$FOLDERS/A$i-f$j/constant
	ln -s ${PWD}/$mesh_dir/system ${PWD}/$FOLDERS/A$i-f$j/system
	ln -s ${PWD}/$mesh_dir/pre_processing ${PWD}/$FOLDERS/A$i-f$j/pre_processing
	ln -s ${PWD}/$mesh_dir/sim_processing ${PWD}/$FOLDERS/A$i-f$j/sim_processing
	cp -r ${PWD}/$mesh_dir/0 ${PWD}/$FOLDERS/A$i-f$j/0
	cp -r ${PWD}/$mesh_dir/change_param ${PWD}/$FOLDERS/A$i-f$j/change_param
	
	cd ./$FOLDERS/A$i-f$j/
	echo -e "Amplitude = $i  frequency = $j"
	./change_param ch_amp $i
	./change_param ch_fq $j
	#----------------------------------------------------------------------------#		
# creates jobscript in each folder	
cat > jobscript.sh <<EOF
#!/bin/bash -l
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name=A$i-f$j
#SBATCH --ntasks-per-node=4

module load singularity/3.6.0rc2
module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

singularity run of2006-py1.6-cpu.sif ./pre_processing ./$FOLDERS/A$i-f$j/
mpirun -np 4 singularity run of2006-py1.6-cpu.sif ./sim_processing ./$FOLDERS/A$i-f$j/
EOF
	chmod +x jobscript.sh
#----------------------------------------------------------------------------#	
	cd ../../../../..	
done
