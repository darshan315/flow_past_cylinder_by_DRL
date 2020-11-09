import numpy as np
import matplotlib.pyplot as plt
import os


def lsh(n, a, b):
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


n = 4  # number of data point

fq_lim = [3, 15]
amp_lim = [0.1, 3.5]

fq = np.round(lsh(n, fq_lim[0], fq_lim[1]), 3)
amp = np.round(lsh(n, amp_lim[0], amp_lim[1]), 3)

# lsh_plt_data(n, fq_lim, amp_lim, fq, amp)

w_d = "~/DRL_Activeflow/test_cases/run/oscillatory_parameter_study_cluster/newnew/"  # home path
folder = "test_cases/run/oscillatory_parameter_study"
path = w_d + folder
ad = lambda d: d + "/cases"
case_dir = ad(path)

for i in amp:
    for j in fq:
        os.system("mkdir -p %s/A%.3f-f%.3f" % (case_dir, i, j))

        os.system("ln -s %s/base_pre-mesh/constant %s/A%.3f-f%.3f/constant" % (path, case_dir, i, j))
        os.system("ln -s %s/base_pre-mesh/system %s/A%.3f-f%.3f/system" % (path, case_dir, i, j))
        os.system("ln -s %s/base_pre-mesh/sim_processing %s/A%.3f-f%.3f/sim_precessing" % (path, case_dir, i, j))
        os.system("ln -s %s/base_pre-mesh/pre_processing %s/A%.3f-f%.3f/pre_processing" % (path, case_dir, i, j))

        os.system("cp -r %s/base_pre-mesh/0 %s/A%.3f-f%.3f/ " % (path, case_dir, i, j))
        os.system("cp -r %s/base_pre-mesh/change_param %s/A%.3f-f%.3f/" % (path, case_dir, i, j))

        os.system("echo -e '\nAmplitude = %.3f  frequency = %.3f' " % (i, j))
        os.system(
            "cd %s/A%.3f-f%.3f/ && ./change_param ch_amp %.3f && ./change_param ch_fq  %.3f" % (case_dir, i, j, i, j))

        with open('%s/A%.3f-f%.3f/jobscript.sh' % (ad(folder), i, j), 'w') as f:
            f.write('''#!/bin/bash -l
        #SBATCH --partition=standard
        #SBATCH --nodes=1
        #SBATCH --time=12:00:00
        #SBATCH --job-name=A%.2ff%.2f
        #SBATCH --ntasks-per-node=2

        module load singularity/3.6.0rc2
        module load mpi/openmpi/4.0.1/cuda_aware_gcc_6.3.0

        singularity run of2006-py1.6-cpu.sif ./pre_processing ./%s/A%.3f-f%.3f/
        mpirun -np 2 singularity run of2006-py1.6-cpu.sif ./sim_processing ./%s/A%.3f-f%.3f/
        ''' % (i, j, ad(folder), i, j, ad(folder), i, j))
        os.system("chmod +x %s/A%.3f-f%.3f/jobscript.sh" % (ad(folder), i, j))
