# Active flow control of the flow past a cylinder using OpenFOAM and PyTorch

## Overview
project overview, structure of this repository, a nice eye-catching picture or animation, scientific goals (you may use the task list as reference) and progress

## Dependencies
- packages/libraries, e.g. Docker

## Getting started

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

## References
