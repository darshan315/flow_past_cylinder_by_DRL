# Active flow control of the flow past a cylinder using OpenFOAM and PyTorch

## Overview
project overview, structure of this repository, a nice eye-catching picture or animation, scientific goals (you may use the task list as reference) and progress

## Dependencies
- packages/libraries, e.g. Docker

## Getting started

### Running simulations with OpenFOAM

To create the Docker container containing *OpenFOAM* and *PyTorch*, execute the *create_openfoam_container.sh* script:

```
./create_openfoam_container.sh
```

Once the environment is created, the typical commands to run a test case look as follows:

```
# start the container and log in
./start_openfoam.sh
# now we are executing commands inside the container
cd test_cases
# the run folder is ignored from the version control system
mkdir run
# create a copy of one of the test cases and run it
cp -r cylinder2D_base run/
cd cylinder2D_base
./Allrun
```

### Starting Jupyterlab

To create the Jupyterlab environment, run:

```
./create_jupyter_container.sh
```

The output of docker container ls --all should contain an entry similar to the following line:

```
ff2822e10fd2    andreweiner/juypter_darshan:v1  "/bin/bash" 7 seconds ago   Up 6 seconds    0.0.0.0:8000->8000/tcp, 8888/tcp jupyter-v1
```

Once the container has been created successfully, the environment can be accessed using the start_notebooks.sh script:

```
./start_notebooks.sh
```

A url with the syntax http://127.0.0.1:8000/?token=... will be displayed in the console. By opening the url in a web browser of your choice, the Jupyter notebooks can be accessed and executed.

## References
