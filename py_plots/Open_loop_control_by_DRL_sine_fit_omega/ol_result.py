import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 160
mpl.rc('text', usetex=True)

f1 = "coef_uc.dat"
f2 = "coef_ol.dat"
f3 = "coef_cl.dat"
f4 = "coef_sf.dat"

cases = ['uncontrolled', 'open-loop controlled', 'closed-loop controlled', 'open-loop with DRL sine-fit parameters']

data = {cases[0]: np.loadtxt(f1, unpack=True, usecols=[0, 1, 3]),
        cases[1]: np.loadtxt(f2, unpack=True, usecols=[0, 1, 3]),
        cases[2]: np.loadtxt(f3, unpack=True, usecols=[0, 1, 3]),
        cases[3]: np.loadtxt(f4, unpack=True, usecols=[0, 1, 3])
        }

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(data[cases[0]][0], data[cases[0]][1], "-.", color= '#1f77b4', linewidth=1.2, markevery=70, label=cases[0])

ax.plot(data[cases[1]][0], data[cases[1]][1], ":", color= '#ff7f0e', linewidth=1.2, markevery=70, label=cases[1])

ax.plot(data[cases[2]][0], data[cases[2]][1], "--", color= '#2ca02c', linewidth=1.2, markevery=70, label=cases[2])

ax.plot(data[cases[3]][0], data[cases[3]][1], "-", color= '#d62728', linewidth=1.2, markevery=70, label=cases[3])

ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

ax.set_xlim((0, 8))
#ax.set_ylim((2.965, 3.26))
ax.set_ylim((2.0, 6))
ax.set_ylabel(r"$c_D$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('cd.png')

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(data[cases[0]][0], data[cases[0]][2], "-.", color= '#1f77b4', linewidth=1.2, markevery=70, label=cases[0])

ax.plot(data[cases[1]][0], data[cases[1]][2], ":", color= '#ff7f0e', linewidth=1.2, markevery=70, label=cases[1])

ax.plot(data[cases[2]][0], data[cases[2]][2], "--", color= '#2ca02c', linewidth=1.2, markevery=70, label=cases[2])

ax.plot(data[cases[3]][0], data[cases[3]][2], "-", color= '#d62728', linewidth=1.2, markevery=70, label=cases[3])

ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

ax.set_xlim((0, 8))
ax.set_ylim((-1.4, 1.6))
ax.set_ylabel(r"$c_L$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('cl.png')
