# Active flow control of the flow past a cylinder using OpenFOAM and PyTorch

## Overview
project overview, structure of this repository, a nice eye-catching picture or animation, scientific goals (you may use the task list as reference) and progress

## Dependencies
- packages/libraries, e.g. Docker, paraview(for visualisation)

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

=======

## Interactive mesh file:
In This Repository interactive mesh.sh file can be found. In this file interpreter is set to ```!/usr/bin/bash``` which is 
mostly common in linux. For windows the default interpreter can be founded by command ``` $ whereis bash ```.
This interactive mesh file is very helpful for mesh study. The shell script is also removing old mesh file in order to
 prevent the conflicts. To be specific the Mesh attributes like cell numbers in ```blockMesh``` and simpleGrading 
 values can be directly changed with one line and with execution of ```mesh.sh``` file in terminal. More details can be found as follows.

### Execution of mesh.sh
```mesh.sh``` script can be executed with four arguments.
+ Argument 1 : bmcell

This argument is able to change the cell numbers in blockMesh file. The line for cell number in blockMesh file reads as:

```hex (0 1 2 3 4 5 6 7) (300 50 1) simpleGrading (1 1 1)```

In above line (300 50 1) represents the cell numbers in x, y and z direction respectively. As the setup is 2D, there will be only 1 cell in z direction.
cell numbers in y-direction can be calculated by the equation shown below. Making value in y-direction dependent to value in x-direction will also prevent the conflict between snappyHexMesh and blockMeshDict. 


![](https://latex.codecogs.com/svg.latex?blockX=blocksX&space;\times&space;\frac{lengthY}{lengthX})

Hence the value for x axis need to change only and value in y-direction will be calculated by this equation. To change this values shell script should be executed as follows with the following values:

```$ ./mesh bmcell 200```

This command will change the line of ```blockMesh``` as shown below and all mesh files like ```blockMesh``` and 
```snappyHexMesh``` will be executed with the change, so one does not have to execute them separately.

```hex (0 1 2 3 4 5 6 7) (200 37 2) simpleGrading (1 1 1)```

+ Argument 2 : bmgrad

This argument is able to change the values of simpleGrading in blockMesh file. The line for simpleGrading in blockMesh file reads as:
more information about simpleGrading can be found [here](https://openfoam.com/documentation/user-guide/blockMesh.php).

```hex (0 1 2 3 4 5 6 7) (300 50 1) simpleGrading (1 1 1)```

In above line simpleGrading (1 1 1) values can be changed with the following execution.

```$ ./mesh bmgrad 2 2 2```

The output will change the attributes in line of ```blockMesh``` as shown below and as explained above all mesh files will be executed consequently.

```hex (0 1 2 3 4 5 6 7) (200 37 1) simpleGrading (2 2 2)```

+ Argument 3 : bmboth

This argument includes combination of both argument 1 and argument 2. This argument is able to change both cell number values and simpleGrading values.
It can be executed as follows :
 
```$ ./mesh bmgrad 350 2 2 2```

In this first argument of value represents values of cell number in x direction and other 3 represent the values of simpleGrading.
It will change code -

From :```hex (0 1 2 3 4 5 6 7) (200 37 1) simpleGrading (1 1 1)```

To:
```hex (0 1 2 3 4 5 6 7) (350 65 10) simpleGrading (2 2 2)```

Argument 4 : spsurf

In this argument the values correspond to refinement of mesh by adjusting refinementSurfaces. More details about snappyHexMesh and refinementSurfaces can be found [here](https://openfoam.com/documentation/user-guide/snappyHexMesh.php).
It can be executed as :
 
```$ ./mesh spsurf 3 3```

This command will change values as shown below and as explained above ll mesh files will be executed consequently.

From :
```level (2 2)```

To:
```level (3 3)```


#### special case :
If no argument is supplied along with execution of command then it will automatically ask for input from users:
Examples of inputs are shown below.
+ This shows User interface for mesh refinement for blockMesh.
```
[user@user cylinder2D_base]$ ./mesh
Defaulf mesh settings is applied. Do you want to refine? [y|n] y
 In which mesh do you want to refine : 
1) blockMesh
2) snappyHexMesh surface
Enter the number of choise : 1

1) blockMesh simpleGrading 
2) blockMesh cell numbers 
3) Both
Enter choise : 1
Enter the cell number(x): 

val

250

Running Mesh
```
+ This shows User interface for mesh refinement for snappyHexMesh.
```
[user@user cylinder2D_base]$ ./mesh
Defaulf mesh settings is applied. Do you want to refine? [y|n] y
 In which mesh do you want to refine : 
1) blockMesh
2) snappyHexMesh surface
Enter the number of choise : 2
Enter the level values: 

val1 val2

3 3

Running Mesh

## References

