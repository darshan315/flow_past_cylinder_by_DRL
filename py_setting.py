import numpy as np
import matplotlib.pyplot as plt
import os


def lsh(n, a, b):
    """
    lhs stands for Latin hypercube sampling.
    it is used to generate evenly distributed samples over multidimensional data space.
    :param n: number of sample
    :param a: lower bound of data space eg. [a,b] = [0,1]
    :param b: higher bound of data space eg. [a,b] = [0,1]
    :return:
    referance : https://youtu.be/r6rp-Qxc9xI
    """
    l_lim = np.arange(a, b, (b - a) / n)
    u_lim = np.arange(a + (b - a) / n, b + (b - a) / n, (b - a) / n)
    p = np.random.uniform(low=l_lim, high=u_lim, size=[n])
    np.random.shuffle(p)
    return p


def lsh_plt_data(n, a, b, data1, data2):  # a, b list here.
    plt.figure(figsize=[5, 5])
    plt.xlim([a[0], a[1]])
    plt.ylim([b[0], b[1]])
    plt.scatter(data1, data2, c='r')

    for i in np.arange(a[0], a[1], (a[1] - a[0]) / n):
        plt.axvline(i)
    for i in np.arange(b[0], b[1], (b[1] - b[0]) / n):
        plt.axhline(i)
    plt.savefig('data_vis.png')


n = 5  # number of data point

fq_lim = [3, 15]
amp_lim = [0.1, 3.5]

fq = np.round(lsh(n, fq_lim[0], fq_lim[1]), 3)
amp = np.round(lsh(n, amp_lim[0], amp_lim[1]), 3)

lsh_plt_data(n, fq_lim, amp_lim, fq, amp)

w_d = "~/DRL_Activeflow/"  # home path
folder = "test_cases/run/oscillatory_parameter_study"
path = w_d + folder

def ad(d): return d + "/cases"
case_dir = ad(path)

for t in range(len(amp)):
    i = amp[t]
    j = fq[t]
    os.system(f"mkdir -p {case_dir}/A{i:.3f}-f{j:.3f} &&")
    os.system(f"ln -s {path}/base_pre-mesh/constant {case_dir}/A{i:.3f}-f{j:.3f}/constant &&"
              f"ln -s {path}/base_pre-mesh/system {case_dir}/A{i:.3f}-f{j:.3f}/system &&"
              f"ln -s {path}/base_pre-mesh/change_param {case_dir}/A{i:.3f}-f{j:.3f}/sim_processing &&"
              f"ln -s {path}/base_pre-mesh/change_param {case_dir}/A{i:.3f}-f{j:.3f}/pre_processing")
    os.system(f"cp -r {path}/base_pre-mesh/0 {case_dir}/A{i:.3f}-f{j:.3f}/ &&"
              f"cp -r {path}/base_pre-mesh/change_param {case_dir}/A{i:.3f}-f{j:.3f}/")

    os.system(f"cd {case_dir}/A{i:.3f}-f{j:.3f}/ &&"
              f"echo -e \"\nAmplitude = {i:.3f}  frequency = {j:.3f} \n\" &&"
              f"./change_param ch_amp {i:.3f} &&"
              f"./change_param ch_fq  {j:.3f}")
    os.system("touch test.txt")
    with open(f'{ad(folder)}/A{i:.3f}-f{j:.3f}/jobscript.sh', 'w') as rsh:
        rsh.write(f'''#!/bin/bash -l
        # SBATCH --partition=standard
        # SBATCH --nodes=1
        # SBATCH --time=12:00:00
        # SBATCH --job-name=A{i:.2f}f{j:.2f}
        # SBATCH --ntasks-per-node=4

        module load singularity/3.6.0rc2
        module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

        singularity run of2006-py1.6-cpu.sif ./pre_processing {ad(folder)}/A{i:.3f}-f{j:.3f}/
        mpirun -np 4 singularity run of2006-py1.6-cpu.sif ./sim_processing {ad(folder)}/A{i:.3f}-f{j:.3f}/
        ''')
    os.system(f"chmod +x {ad(folder)}/A{i:.3f}-f{j:.3f}/jobscript.sh")
    os.system("sed -i 's;        ;;' %s/A%.3f-f%.3f/jobscript.sh" % (ad(folder), i, j))
