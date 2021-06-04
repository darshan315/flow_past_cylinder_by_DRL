from pandas import read_csv
from glob import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.animation import FuncAnimation

mpl.rcParams['figure.dpi'] = 160
mpl.rc('text', usetex=True)


def read_surface_data(file_path):
    columns = ["x", "y", "z", "p"]
    data = read_csv(file_path, sep=" ", names=columns, skiprows=[0, 1], header=None)
    return data[data.z > 0.015][["x", "y", "p"]]


def get_write_times(data_path):
    time_folders = glob(data_path + "*")
    times = [folder.split("/")[-1] for folder in time_folders]
    return sorted(times, key=float)


def compute_polar_coordinates(x, y, c_x, c_y):
    x = x - c_x
    y = y - c_y
    radius = np.sqrt(np.square(x) + np.square(y))
    theta = np.where(y >= 0, np.arccos(x / radius), 2.0 * np.pi - np.arccos(x / radius))
    return radius, theta


data_path = "./surface/"
times = get_write_times(data_path)
print(f"Found {len(times)} time folders.")

ol_data_path = "./surface_ol/"

cl_data_path = "./surface_cl/"

start_time = [times[534], times[542], times[550], times[558]]

t_time = [5.34, 5.42, 5.50, 5.58]
alphas = [0.2, 0.45, 0.6, 1]


def get_datas(i):
    file_path = data_path + start_time[i] + "/p_airfoil.raw"
    data = read_surface_data(file_path)
    rad, theta = compute_polar_coordinates(data.x.values, data.y.values, 0.2, 0.2)

    theta_sorting = np.argsort(theta)
    theta_sorted = theta[theta_sorting]
    rad_sorted = rad[theta_sorting]
    p_sorted = data.p.values[theta_sorting]
    theta_sorted = np.concatenate((theta_sorted, theta_sorted[:1]))
    rad_sorted = np.concatenate((rad_sorted, rad_sorted[:1]))
    p_sorted = np.concatenate((p_sorted, p_sorted[:1]))

    return theta_sorted, p_sorted


def get_ol_datas(i):
    file_path = ol_data_path + start_time[i] + "/p_airfoil.raw"
    data = read_surface_data(file_path)
    rad, theta = compute_polar_coordinates(data.x.values, data.y.values, 0.2, 0.2)

    theta_sorting = np.argsort(theta)
    theta_sorted = theta[theta_sorting]
    rad_sorted = rad[theta_sorting]
    p_sorted = data.p.values[theta_sorting]
    theta_sorted = np.concatenate((theta_sorted, theta_sorted[:1]))
    rad_sorted = np.concatenate((rad_sorted, rad_sorted[:1]))
    p_sorted = np.concatenate((p_sorted, p_sorted[:1]))

    return theta_sorted, p_sorted


def get_cl_datas(i):
    file_path = cl_data_path + start_time[i] + "/p_airfoil.raw"
    data = read_surface_data(file_path)
    rad, theta = compute_polar_coordinates(data.x.values, data.y.values, 0.2, 0.2)

    theta_sorting = np.argsort(theta)
    theta_sorted = theta[theta_sorting]
    rad_sorted = rad[theta_sorting]
    p_sorted = data.p.values[theta_sorting]
    theta_sorted = np.concatenate((theta_sorted, theta_sorted[:1]))
    rad_sorted = np.concatenate((rad_sorted, rad_sorted[:1]))
    p_sorted = np.concatenate((p_sorted, p_sorted[:1]))

    return theta_sorted, p_sorted


fig, ax = plt.subplots(1, 1, figsize=(7, 7), subplot_kw={'projection': 'polar'})

for i in range(4):
    theta_sorted, p_sorted = get_datas(i)
    ln, = ax.plot(theta_sorted + np.pi, p_sorted, color="b", linestyle=':', alpha=alphas[i])
for i in range(4):
    theta_sorted, p_sorted = get_ol_datas(i)
    ln, = ax.plot(theta_sorted + np.pi, p_sorted, color="g", linestyle='--', alpha=alphas[i])
for i in range(4):
    theta_sorted, p_sorted = get_cl_datas(i)
    ln, = ax.plot(theta_sorted + np.pi, p_sorted, color="r", linestyle='-', alpha=alphas[i])

ax.grid(True)
ax.set_theta_zero_location("W")
ax.set_rlim(-2.0, 0)
ax.set_rticks(np.linspace(-1.4, 0, 5))
ax.set_xlabel(r"$p$")
ax.text(-0.01, -0.3, r"flow direction $\rightarrow$")

plt.savefig('results.png')
