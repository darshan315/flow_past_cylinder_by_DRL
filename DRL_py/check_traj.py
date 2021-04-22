from glob import glob
import pandas as pd
import os


def check_trajectories(sample):
    """
    Check whether the trajectory is completed.
    In case trajectory fail to complete then delete specific trajectory.
    """

    traj_files = glob(f'./env/sample_{sample}' + "/*/")

    corrupted_traj = []
    completed_traj = []

    for i, traj in enumerate(traj_files):

        if os.path.isfile(traj_files[i] + "trajectory.csv"):
            completed_traj.append(traj)

            x_traj = pd.read_csv(traj_files[i] + "trajectory.csv", sep=",", header=0)
            t_l = len(x_traj.t.values)

            if t_l >= 500:
                completed_traj.append(traj)
            else:
                corrupted_traj.append(traj)
        else:
            corrupted_traj.append(traj)

    for traj in corrupted_traj:
        os.system(f"rm -r {traj}")
