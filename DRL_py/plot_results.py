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

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(11,8))

ax1.plot(iterations, rewards_mean)
ax1.fill_between(iterations, rewards_mean - rewards_std, rewards_mean + rewards_std, color='#888888', alpha=0.4)
ax1.set_xlabel("Iteration of PPO")
ax1.set_ylabel("Mean of rewards")


ax2.plot(iterations, rewards_10_mean)
ax2.fill_between(iterations, rewards_10_mean - rewards_10_std, rewards_10_mean + rewards_10_std, color='#888888', alpha=0.4)
ax2.set_xlabel("Iteration of PPO")
ax2.set_ylabel("Mean of last 10 rewards")

ax3.plot(iterations, rewards_100_mean)
ax3.fill_between(iterations, rewards_100_mean - rewards_100_std, rewards_100_mean + rewards_100_std, color='#888888', alpha=0.4)
ax3.set_xlabel("Iteration of PPO")
ax3.set_ylabel("Mean of last 100 rewards")

plt.savefig('results.png')
