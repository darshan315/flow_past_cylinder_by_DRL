"""
    This file to run trajectory, hence handling OpenFOAM files and executing them in machine

    called in : replay_buffer.py
"""

import _thread
import os
import queue
import subprocess

import numpy as np


class env:
    """
        This Class is to run trajectory, hence handling OpenFOAM files and executing them in machine
    """
    def __init__(self, n_worker, buffer_size, control_between):
        """

        Args:
            n_worker: no of trajectories at the same time (worker)
            buffer_size: total number of trajectories
            contol_between: random starting point range of action in trajectory
        """
        self.n_worker = n_worker
        self.buffer_size = buffer_size
        self.control_between = control_between

    def write_jobfile(self, job_name, file, job_dir):
        with open(f'{job_dir}/jobscript.sh', 'w') as rsh:
            rsh.write(f"""#!/bin/bash -l        
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --job-name={job_name}
#SBATCH --ntasks-per-node=4

module load singularity/3.6.0rc2

singularity run ../of2006-py1.6-cpu.sif {file} {job_dir}""")

        os.system(f"chmod +x {job_dir}/jobscript.sh")

    def rand_n_to_contol(self, n):
        """
        To get the random number from the range -> .2f%

        Args:
            n: number of random sampled number (in this case n=1)

        Returns: random number

        """
        np.random.seed()
        n_rand = np.random.uniform(self.control_between[0], self.control_between[1], n)
        n_rand = np.round(n_rand, 2)
        return n_rand

    def process_waiter(self, proc, job_name, que):
        """
             This method is to wait for the executed process till it is completed
         """
        try:
            proc.wait()
        finally:
            que.put((job_name, proc.returncode))

    def run_trajectory(self, buffer_counter, proc, results, sample):
        """
        To run the trajectories

        Args:
            buffer_counter: which trajectory to run (n -> traj_0, traj_1, ... traj_n)
            proc: array to hold process waiting flag
            results: array to hold process finish flag
            sample: number of iteration of main ppo

        Returns: execution of OpenFOAM Allrun file in machine

        """
        # get the random start
        rand_control_traj = self.rand_n_to_contol(1)

        # changing of end time to keep trajectory length equal
        endtime = round(float(rand_control_traj[0] + 5), 2)

        # make dir for new trajectory
        traj_path = f"./env/sample_{sample}/trajectory_{buffer_counter}"
        print(f"\n starting trajectory : {buffer_counter} \n")
        os.makedirs(traj_path, exist_ok=True)

        # copy files form base_case
        # change starting time of control -> 0.org/U && system/controlDict
        # change of ending time -> system/controlDict
        os.popen(f'cp -r ./env/base_case/agentRotatingWallVelocity/* {traj_path}/ && '
                 f'sed -i "s/startTime.*/startTime       {rand_control_traj[0]};/g" {traj_path}/0.org/U &&'
                 f'sed -i "/^endTime/ s/endTime.*/endTime         {endtime};/g" {traj_path}/system/controlDict &&'
                 f'sed -i "s/timeStart.*/timeStart       {rand_control_traj[0]};/g" {traj_path}/system/controlDict')

        self.write_jobfile(job_name=f'traj_{buffer_counter}', file='./Allrun', job_dir=traj_path+'/')
        jobfile_path = f'{traj_path}' + '/jobscript.sh'

        proc[buffer_counter] = subprocess.Popen(['sh', 'submit_job.sh', jobfile_path])
        _thread.start_new_thread(self.process_waiter,
                                 (proc[buffer_counter], f"trajectory_{buffer_counter}", results))

    def sample_trajectories(self, sample):
        """

        Args:
            sample: main ppo iteration counter

        Returns: execution of n number of trajectory (n = buffer_size)

        """
        # set the counter to count the numbre of trajectory
        buffer_counter = 0

        # list for the status of trajectory running or finished
        proc = []

        # set the n_workers
        for t in range(int(self.buffer_size)):
            item = "proc_" + str(t)
            proc.append(item)

        # get status of trajectory
        results = queue.Queue()
        process_count = 0

        # execute the n = n_workers trajectory simultaneously
        for n in np.arange(self.n_worker):
            self.run_trajectory(buffer_counter, proc, results, sample)
            process_count += 1
            # increase the counter of trajectory number
            buffer_counter += 1

        # check for any worker is done. if so give next trajectory to that worker
        while process_count > 0:
            job_name, rc = results.get()
            print("job : ", job_name, "finished with rc =", rc)
            if self.buffer_size > buffer_counter:
                self.run_trajectory(buffer_counter, proc, results, sample)
                process_count += 1
                buffer_counter += 1
            process_count -= 1


if __name__ == "__main__":
    n_worker = 2
    buffer_size = 4
    control_between = [0.1, 4]
    sample = 0
    env = env(n_worker, buffer_size, control_between)
    env.sample_trajectories(sample)
