# Active flow control of the flow past a cylinder using OpenFOAM and PyTorch

## Overview
Active flow control is high dimensional optimization problem. Therefore in a generic example as flow around cylinder, the deep reinforcement learning is used to achieve optimal flow control by leveraging its power of approximation in high dimensional space. In this study, the flow control is achieved by open-loop control and closed-loop control. For flow around 2D cylinder, the von kármán vortices impose fluctuating drag and lift forces. Hence, for flow control the objective is to reduce drag and fluactuation of drag and lift for the stability of a cylinder. Hence, the cylinder is rotated in order to control the flow. For open-loop control the optimal strategy is determined by parametric study, where the rotation of the rotation of the cylinder is wave function in order to counter the natural vrtex shedding. For closed-loop control, the flow control is achieved by usind deep reinforcement learning. The proximal policy optimization (PPO) algorithm is used to implement the DRL setup, where the cylinder is rotated with optimal policy network and the **pressure sensors are placed on the surface of the cylinder**. In the PPO iteration, the starting of trajectory control is considered randomly between t=0s and t=4s.

![Screenshot from 2021-06-04 17-42-02](https://user-images.githubusercontent.com/50383431/120828085-65c4ee00-c55c-11eb-833d-7d7b5f7dcf2e.png)



![cd](https://user-images.githubusercontent.com/50383431/120820544-f0a1ea80-c554-11eb-8976-09f36396aef6.png)
![cl](https://user-images.githubusercontent.com/50383431/120820560-f3044480-c554-11eb-8ef6-1a7758e3c9f9.png)

https://user-images.githubusercontent.com/50383431/120820584-f8618f00-c554-11eb-86ec-4874d0bbc636.mp4

![Screenshot from 2021-06-04 17-22-25](https://user-images.githubusercontent.com/50383431/120825424-aa9b5580-c559-11eb-8e0c-9b9baddc7462.png)

![inte_omegas](https://user-images.githubusercontent.com/50383431/120827221-83458800-c55b-11eb-9805-adca1c178c31.png)

## Dependencies
- Python-libraries, Singularity, Docker, paraview(for visualisation)

## Simulation setup

For the simulation setup in OpenFOAM, the base case for the simulation may be found in `./test_cases/cylinder2D_base`. For more info see [here.](https://ml-cfd.com/2020/12/29/running-pytorch-models-in-openfoam-basic-setup-and-examples/)

To Built the singularity image follow the instruction given [here](https://github.com/AndreWeiner/of_pytorch_docker). The singularity image file (.sif) should be in parent directory. 

This base case is executable with singularity image as,

``` singuarity run of2006-py1.6-cpu.sif ./Allrun ./test_cases/cylinder2D_base/ ```

For mesh dependency study, execute the shell file as,

``` $ ./mesh_study ```

The mesh is set to refinement level 100, 200, and 400. For more refinement level change the array `mesh_size=( 100 200 400 )` in shell script. The simulations for different mesh will generate in `./test_case/run/mesh_convergence_study/`.

## Open-loop control
The parameter amplitude and frequency for the rotation of the cylinder is sampled by LHS method. For LHS sampling,

option-1 (with shell script)

``` $ ./bash_LHS_sampling ```

option-2 (with python script)

``` $ python3 py_LHS_sampling.py ```

for python script the py-libraries - numpy and matplotlib.

The simulations for the LHS is found in `./test_cases/run/oscillatory_parameter_study/cases`.

## Closed-loop control by Deep Reinforcement Learning using PPO

### Training on local machine

#### python-libraries :

Python libraries that are used in DRL can be saperately installed in virtual environment by,

``` pip install -r ./DRL_py/docker/requirements.txt ```

#### PPO iterations

For PPO iteration, the simulations in OpenFOAM (environmnent) are handled by `./DRL_py/env_local.py`. 

To set the triaing in local machine, in `./DRL_py/reply_buffer.py`, change `machine` variable to `machine = 'local'`. see [here.](https://github.com/darshan315/flow_past_cylinder_by_DRL/blob/0ece783bc40f56bd9eaae628471d96c3856221a4/DRL_py/reply_buffer.py#L14)

To start training,

`$ python3 main.py`

#### Training on cluster (slurm workload manager)

#### python-libraries :

Python libraries in cluster is installed by creating virtual environment as,

```
module load python/3.7 
python3 -m pip install --user virtualenv 
python3 -m virtualenv venv
```
To activate the virtual environment :
```
source venv/bin/activate
```
To deactivate :
```
deactivate
```
To install the python libraries in `venv` virtual environment,

``` pip install -r ./DRL_py/docker/requirements.txt ```

#### PPO iterations

For PPO iteration on cluster, the simulations in OpenFOAM (environmnent) are handled by `./DRL_py/env_cluster.py`. 

To set the training on cluster, in `./DRL_py/reply_buffer.py`, change `machine` variable to `machine = 'cluster'`. see [here.](https://github.com/darshan315/flow_past_cylinder_by_DRL/blob/0ece783bc40f56bd9eaae628471d96c3856221a4/DRL_py/reply_buffer.py#L14)

To submit the training job on cluster,

`$ cd DRL_py`

`$ sbatch python_job.sh`

## Report
The report for this study : https://doi.org/10.5281/zenodo.4897961

BibTex citation :
```
@misc{darshan_thummar_2021_4897961,
  author       = {Darshan Thummar},
  title        = {{Active flow control in simulations of fluid flows 
                   based on deep reinforcement learning}},
  month        = may,
  year         = 2021,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.4897961},
  url          = {https://doi.org/10.5281/zenodo.4897961}
}
```
## References
The PPO implementation is based on chapter 12 of Miguel Morales' excellent book *Grokking Deep Reinforcement Learning*. For more information refer to [the Notebook](https://github.com/mimoralea/gdrl).

For more information about the base simulation setup and the open loop control refer [Schaefer  et al.](https://link.springer.com/chapter/10.1007/978-3-322-89849-4_39), and [Tokumaru et al.](https://authors.library.caltech.edu/67622/1/Tokumaru_Dimotakis.1991.JFM.Rotary%20oscillation%20control%20of%20a%20cylinder%20wake.pdf) The robust active flow control is inspired from [Rabault et al.](https://arxiv.org/pdf/1808.07664.pdf), and [Tokarev et al.](https://www.mdpi.com/1996-1073/13/22/5920)
