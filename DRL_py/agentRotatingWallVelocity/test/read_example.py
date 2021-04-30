#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

# read trajectory data
## number of cell faces forming the cylinder patch
n_faces = 54
names = ["t", "omega", "omega_mean", "omega_log_std", "log_p", "entropy", "theta_sum", "dt_theta_sum"]
p_names = ["p{:d}".format(i) for i in range(n_faces)]

trajectory = pd.read_csv("trajectory.csv", sep=",", names=names+p_names, header=0)

## example 1: get pressure values as numpy array; .values converts dataframe to numpy array
## the p array should have the shape [n_time_steps, n_faces]
p = trajectory[p_names].values
print("Shape of p:", p.shape)

## example 2: get logarithmic probabilites as numpy array
## the log_p array should have the shape [n_time_steps]
log_p = trajectory.log_p.values
print("Shape of log_p: ", log_p.shape)

# read force coefficients
names_coeffs = ["col{:d}".format(i) for i in range(13)]
## we only want time, drag, and lift
names_coeffs[0] = "t"
names_coeffs[1] = "c_d"
names_coeffs[3] = "c_l"
keep = ["t", "c_d", "c_l"]

file_path = "postProcessing/forces/0/coefficient.dat"
coeffs = pd.read_csv(file_path, sep="\t", names=names_coeffs, usecols=keep, comment="#")
## for some reason the function object's writeControls do not work properly; therefore,
## we pick only every nth row from the dataframe; this number should be the same as for
## the trajectory (specified in the boundary condition)
pick_every = 20
coeffs = coeffs[coeffs.index % pick_every == 0]
print("Shape of force coefficients: ", coeffs.shape)

## check for some examples if the times are equivalent
print(trajectory.t.values[0], trajectory.t.values[5], trajectory.t.values[-1])
print(coeffs.t.values[0], coeffs.t.values[5], coeffs.t.values[-1])