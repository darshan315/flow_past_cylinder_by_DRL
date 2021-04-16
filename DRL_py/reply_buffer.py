"""
    This file has function to sample the trajectories and extract data,
    as states, rewards, actions, logporbs and rewards, from it.

    called in :  ppo.py
"""

from read_trajectory_data import *
from cal_R_gaes import *
from check_traj import *

# If machine = 'local' then the functions from env_local will be imported
# If machine = 'cluster' then the functions from env_cluster will be imported
machine = 'cluster'

if machine == 'local':
    from env_local import *
elif machine == 'cluster':
    from env_cluster import *
else:
    print('Provide machine')
    assert machine


def fill_buffer(env, sample, n_sensor, gamma, r_1, r_2, r_3, r_4):
    """
    This function is to sample trajectory and get states, actions, probabilities, rewards,
    and to calculate returns.

    Args:
        env: instance of environment class for sampling trajectories
        sample: number of iteration
        n_sensor: no of patches at the surface of cylinder
        gamma: discount factor
        r_1: coefficient for reward function
        r_2: coefficient for reward function
        r_3: coefficient for reward function
        r_4: coefficient for reward function

    Returns: arrays of, states, actions, rewards, returns, probabilities

    """

    # to sample the trajecties
    env.sample_trajectories(sample)
    
    # check the trajectory to be completed
    check_trajectories(sample)

    traj_files = glob(f'./env/sample_{sample}' + "/*/")

    # To check if the trajectories is sampled
    n_traj = len(traj_files)
    assert n_traj > 0

    # To extract the length of trajectories
    t_traj = pd.read_csv(traj_files[0] + "trajectory.csv", sep=",", header=0)

    # due to delayed starting behaviour the time steps set to explicit -> length of trajectory
    # n_T = len(t_traj.t.values)
    n_T = 500

    # buffer initialization
    state_buffer = np.zeros((n_traj, n_T, n_sensor))
    action_buffer = np.zeros((n_traj, n_T - 1))
    reward_buffer = np.zeros((n_traj, n_T))
    return_buffer = np.zeros((n_traj, n_T))
    log_prob_buffer = np.zeros((n_traj, n_T - 1))

    for i, files in enumerate(traj_files):
        # get the dataframe from the trajectories
        coeff_data, trajectory_data, p_at_faces = read_data_from_trajectory(files)

        # state values from data frame
        states = trajectory_data[p_at_faces].values

        # action values from data frame
        actions_ = trajectory_data.omega.values
        actions = actions_[:-1]
        
        # rotation rate
        theta_ = trajectory_data.theta_sum.values
        d_theta = trajectory_data.dt_theta_sum.values

        # rewards and returns from cal_R_gaes.py -> calculate_rewards_returns
        rewards, returns = calculate_rewards_returns(r_1, r_2, r_3, r_4, coeff_data, gamma, theta_, d_theta)

        # log_probs from data frame
        log_probs_ = trajectory_data.log_p.values
        log_probs = log_probs_[:-1]

        # appending values in buffer
        state_buffer[i] = states[:n_T, :]
        action_buffer[i] = actions[:n_T-1]
        reward_buffer[i] = rewards[:n_T]
        return_buffer[i] = returns[:n_T]
        log_prob_buffer[i] = log_probs[:n_T-1]

    return state_buffer, action_buffer, reward_buffer, return_buffer, log_prob_buffer
