import numpy as np
import _thread
import queue
import subprocess
import os


class env:
    def __init__(self, n_worker, buffer_size, base_setup_end_time, trajectory_end_time,
                 base_case_setup, buffer, sample):
        self.n_worker = n_worker
        self.buffer_size = buffer_size
        self.base_setup_end_time = base_setup_end_time
        self.trajectory_end_time = trajectory_end_time
        self.base_case_setup = base_case_setup
        self.buffer = buffer
        self.sample = sample

    def initial_setup(self):
        print("\n Forming base case...\n")
        path = "./env/initial_setup"
        os.makedirs(path, exist_ok=True)
        os.system(f'cp -r ./env/base_case/* {path}/ &&'
                  f'sed -i "/^startTime/ s/startTime.*/startTime       0;/g" {path}/system/controlDict &&'
                  f'sed -i "/^endTime/ s/endTime.*/endTime         {self.base_setup_end_time};/g" {path}/system/controlDict &&'
                  f'singularity run ../of2006-py1.6-cpu.sif ./Allrun {path}/')
        print("\n Initial setup is done... \n")

    def read_data(self, trajectory, buffer):
        path = "./env/trajectories/" + trajectory
        # read coeff.dat file
        # copy data into buffer
        pass

    def clean_trajectory(self, trajectory):
        path = "./env/trajectories/" + trajectory
        # deletes the trajectory
        pass

    def process_waiter(self, proc, job_name, que):
        try:
            proc.wait()
        finally:
            que.put((job_name, proc.returncode))

    def run_trajectory(self, buffer_counter, proc, results):
        traj_path = f"./env/sample_{self.sample}/trajectory_{buffer_counter}"
        print(f"\n starting trajectory : {buffer_counter} \n")
        os.makedirs(traj_path, exist_ok=True)
        os.popen(f'cp -r ./env/initial_setup/* {traj_path}/ && '
                 f'sed -i "/^startFrom/ s/startFrom.*/startFrom       latestTime;/g" {traj_path}/system/controlDict &&'
                 f'sed -i "/^endTime/ s/endTime.*/endTime         {self.trajectory_end_time};/g" {traj_path}/system/controlDict &&'
                 f'rm {traj_path}/log*')
        proc[buffer_counter] = subprocess.Popen(
            ['singularity', 'run', '../of2006-py1.6-cpu.sif', './sim_processing', f'{traj_path}/'])
        _thread.start_new_thread(self.process_waiter,
                                 (proc[buffer_counter], f"trajectory_{buffer_counter}", results))

    def fill_buffer(self):
        buffer_counter = 0
        proc = []
        for t in range(int(self.buffer_size)):
            item = "proc_" + str(t)
            proc.append(item)

        results = queue.Queue()
        process_count = 0

        if base_case_setup:
            self.initial_setup()

        for n in np.arange(self.n_worker):
            self.run_trajectory(buffer_counter, proc, results)
            process_count += 1
            buffer_counter += 1

        while process_count > 0:
            job_name, rc = results.get()
            print("job : ", job_name, "finished with rc =", rc)
            if self.buffer_size > buffer_counter:
                self.read_data(job_name, self.buffer)
                self.clean_trajectory(job_name)
                self.run_trajectory(buffer_counter, proc, results)
                process_count += 1
                buffer_counter += 1
            process_count -= 1


if __name__ == "__main__":
    n_worker = 1
    buffer_size = 2
    base_setup_end_time = 0.2
    trajectory_end_time = 0.4
    base_case_setup = True
    buffer = []
    sample = 1
    env = env(n_worker, buffer_size, base_setup_end_time, trajectory_end_time, base_case_setup, buffer, sample)
    #  fór loop for multiple sample : var : sample
    env.fill_buffer()
