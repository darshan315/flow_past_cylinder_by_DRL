import numpy as np
import subprocess
import os.path
import time
from network import *


def get_states():
    # get states 2d array (size of presure probe x no. of trajectory)
    states = np.random.randint(10, 100, (10, 1, 10))
    return states


def get_action(states):
    in_dim = [states.shape[0], states.shape[1]]
    out_dim = 1
    policy_model = FCCA(in_dim, out_dim, hidden_dims=(64, 64))
    actions, logpas, are_exploratory = policy_model.np_pass(states)
    return actions


def cal_reward():
    # reading coefficient.dat file and extract cd and cl and calculating reward
    pass


def initial_setup():
    n = 10
    lim_a = 4
    lim_b = 5

    traj = np.arange(n)

    s = np.arange(lim_a, lim_b, 0.01)

    p0 = subprocess.run(['sh', 'link_to_container.sh'], check=True)
    t_list = []
    t_name = []
    for i in range(n):
        t = np.random.choice(s, replace=False).round(2)
        p1 = subprocess.run(['sh', 'trajectory_starting_setup.sh', str(i), str(t)], check=True)
        t_list.append(t)

    # p2 = subprocess.run(['sh', 'executing_jobs.sh'], check=True)

    for i in range(n):
        t_path = 'env/trajectories/trajectory_' + str(i) + '_' + str(t_list[i])
        t_name.append(t_path + '/done.txt')
        while not os.path.exists(t_path + '/done.txt'):
            time.sleep(1)

        if os.path.isfile(t_path + '/done.txt'):
            print(open(r"done.txt", "r").read())
        else:
            raise ValueError("%s isn't a file!" % t_path + '/done.txt')
    return t_name, t_list


def step_in_env(dirs, t_array):
    states = get_states()

    action = get_action(states)
    action = action[:, 0]

    for i, item in enumerate(t_array):
        p3 = subprocess.run(['sh', 'impl_action.sh', str(i), str(item), str(action[i])], check=True)

    # p4 = subprocess.run(['sh', 'executing_jobs.sh'], check=True)

    for i, path in enumerate(dirs):
        while not os.path.exists(path + '/done.txt'):
            time.sleep(1)

        if os.path.isfile(path + '/done.txt'):
            print(open(r"done.txt", "r").read())
        else:
            raise ValueError("%s isn't a file!" % path + '/done.txt')

    rewards = cal_reward()

    return states, action, rewards


dirs, t_array = initial_setup()
state_episode = []
action_episode = []
reward_episode = []
newstate_episode = []

trajectory_len = 100

for i in range(trajectory_len):
    state_tr, action_tr, reward_tr = step_in_env(dirs, t_array)
    new_states = get_states()
    state_episode.append(state_tr)
    action_episode.append(action_tr)
    reward_episode.append(reward_tr)
    newstate_episode.append(new_states)
