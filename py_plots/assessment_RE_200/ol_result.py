import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 160
mpl.rc('text', usetex=True)

f1 = "coef_uc.dat"
f2 = "coef_ol.dat"
f3 = "coef_cl.dat"

cases = ['uncontrolled', 'open-loop controlled', 'closed-loop controlled']

data = {cases[0]: np.loadtxt(f1, unpack=True, usecols=[0, 1, 3]),
        cases[1]: np.loadtxt(f2, unpack=True, usecols=[0, 1, 3]),
        cases[2]: np.loadtxt(f3, unpack=True, usecols=[0, 1, 3])}
'''
cd_mean = np.mean(data[cases[1]][1][-4000:])
cl_mean = np.mean(data[cases[1]][2][-4000:])

cd_max = np.max(data[cases[1]][1][-4000:])
cl_max = np.max(data[cases[1]][2][-4000:])

cd_min = np.min(data[cases[1]][1][-4000:])
cl_min = np.min(data[cases[1]][2][-4000:])

print(f"cd_mean = {cd_mean}, cl_mean = {cl_mean}")
print(f"cd_max = {cd_max}, cl_max = {cl_max}")
print(f"cd_min = {cd_min}, cl_min = {cl_min}")

cd_uc = [3.14741, 3.17212, 3.19653] # [cd_min, cd_mean, cd_max]
cl_uc = [-0.904919, -0.0126599, 0.878955] # [cl_min, cl_mean, cl_max]

cd_mean_percent = (cd_uc[1]-cd_mean)/cd_uc[1] * 100
cd_max_percent = (cd_uc[2]-cd_mean)/cd_uc[2] * 100
cd_min_percent = (cd_uc[0]-cd_mean)/cd_uc[0] * 100

cl_mean_percent = (cl_uc[1]-cl_mean)/cd_uc[1] * 100
cl_max_percent = (cl_uc[2]-cl_max)/cd_uc[2] * 100
cl_min_percent = (cl_uc[0]-cl_min)/cd_uc[0] * 100
'''

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(data[cases[0]][0], data[cases[0]][1], "-.", color= '#1f77b4', linewidth=1.2, markevery=70, label=cases[0])

ax.plot(data[cases[1]][0], data[cases[1]][1], ":", color= '#ff7f0e', linewidth=1.2, markevery=70, label=cases[1])

ax.plot(data[cases[2]][0], data[cases[2]][1], "-", color= '#2ca02c', linewidth=1.2, markevery=70, label=cases[2])

ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

ax.set_xlim((0, 8))
ax.set_ylim((2.38, 3.26))
ax.set_ylabel(r"$c_D$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('cd_assessment.png')

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(data[cases[0]][0], data[cases[0]][2], "-.", color= '#1f77b4', linewidth=1.2, markevery=70, label=cases[0])

ax.plot(data[cases[1]][0], data[cases[1]][2], ":", color= '#ff7f0e', linewidth=1.2, markevery=70, label=cases[1])

ax.plot(data[cases[2]][0], data[cases[2]][2], "-", color= '#2ca02c', linewidth=1.2, markevery=70, label=cases[2])

ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

ax.set_xlim((0, 8))
ax.set_ylim((-2.2, 2.2))
ax.set_ylabel(r"$c_L$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('cl_assessment.png')
