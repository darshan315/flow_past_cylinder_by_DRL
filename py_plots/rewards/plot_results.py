from glob import glob
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['figure.dpi'] = 160
mpl.rc('text', usetex=True)
plt.rcParams.update({'font.size': 7})

folder_path = './results/evaluation/'

files = glob(folder_path + '*')

result = np.zeros((len(files), 6))
iterations = np.arange((len(files)))

paths = []

for i in range(len(files)):
    path = folder_path + 'evaluations_' + f'{i}.npy'
    paths.append(path)

for i, file in enumerate(paths):
    result[i] = np.load(file)

rewards_mean = np.transpose(result)[0]
rewards_std = np.transpose(result)[1]

rewards_10_mean = np.transpose(result)[2]
rewards_10_std = np.transpose(result)[3]

rewards_100_mean = np.transpose(result)[4]
rewards_100_std = np.transpose(result)[5]

fig, (ax1) = plt.subplots(figsize=(11,6))

ax1.plot(iterations, rewards_mean, color='#1f77b4', label=r'mean of rewards')
ax1.fill_between(iterations, rewards_mean - rewards_std, rewards_mean + rewards_std, color='#1f77b4', alpha=0.3, label=r'2 $\sigma$ averaged rewards')
ax1.set_xlabel(r"Iteration of PPO",fontsize=15)
ax1.set_ylabel(r"Mean of rewards",fontsize=15)
ax1.tick_params(labelsize=15)
ax1.legend(loc='lower right', fontsize=15)

plt.savefig('results.png')
