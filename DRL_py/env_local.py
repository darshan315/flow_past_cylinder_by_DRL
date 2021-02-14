import numpy as np
import _thread
import queue
import subprocess


class env:
    def __init__(self, n_worker, buffer_size, base_setup_end_time, trajectory_end_time, base_case_setup, buffer):
        self.n_worker = n_worker
        self.buffer_size = buffer_size
        self.base_setup_end_time = base_setup_end_time
        self.trajectory_end_time = trajectory_end_time
        self.base_case_setup = base_case_setup
        self.buffer = buffer

    def initial_setup(self):
        print("\n Forming base case...\n")
        p = subprocess.run(['sh', 'env_local_initial.sh', str(self.base_setup_end_time)], check=True)
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
            print("\n starting trajectory : {} \n".format(buffer_counter))
            proc[buffer_counter] = subprocess.Popen(
                ['sh', 'start_traj_local.sh', str(buffer_counter), str(trajectory_end_time)])
            _thread.start_new_thread(self.process_waiter,
                                     (proc[buffer_counter], "trajectory_{}".format(buffer_counter), results))
            process_count += 1
            buffer_counter += 1

        while process_count > 0:
            job_name, rc = results.get()
            print("job : ", job_name, "finished with rc =", rc)
            if self.buffer_size > buffer_counter:
                self.read_data(job_name, self.buffer)
                self.clean_trajectory(job_name)
                print("\n starting trajectory : {} \n".format(buffer_counter))
                proc[buffer_counter] = subprocess.Popen(
                    ['sh', 'start_traj_local.sh', str(buffer_counter), str(trajectory_end_time)])
                _thread.start_new_thread(self.process_waiter,
                                         (proc[buffer_counter], "trajectory_{}".format(buffer_counter), results))
                process_count += 1
                buffer_counter += 1
            process_count -= 1


if __name__ == "__main__":
    n_worker = 2
    buffer_size = 4
    base_setup_end_time = 0.2
    trajectory_end_time = 0.4
    base_case_setup = True
    buffer = []
    env = env(n_worker, buffer_size, base_setup_end_time, trajectory_end_time, base_case_setup, buffer)
    env.fill_buffer()
