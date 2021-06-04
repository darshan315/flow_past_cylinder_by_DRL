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


file_path = data_path + times[0] + "/p_airfoil.raw"
data = read_surface_data(file_path)
rad, theta = compute_polar_coordinates(data.x.values, data.y.values, 0.2, 0.2)

theta_sorting = np.argsort(theta)
theta_sorted = theta[theta_sorting]
rad_sorted = rad[theta_sorting]
p_sorted = data.p.values[theta_sorting]
theta_sorted = np.concatenate((theta_sorted, theta_sorted[:1]))
rad_sorted = np.concatenate((rad_sorted, rad_sorted[:1]))
p_sorted = np.concatenate((p_sorted, p_sorted[:1]))


file_path_ol = ol_data_path + times[0] + "/p_airfoil.raw"
data_ol = read_surface_data(file_path_ol)
rad_ol, theta_ol = compute_polar_coordinates(data_ol.x.values, data_ol.y.values, 0.2, 0.2)

theta_sorting_ol = np.argsort(theta_ol)
theta_sorted_ol = theta_ol[theta_sorting_ol]
rad_sorted_ol = rad_ol[theta_sorting_ol]
p_sorted_ol = data_ol.p.values[theta_sorting_ol]
theta_sorted_ol = np.concatenate((theta_sorted_ol, theta_sorted_ol[:1]))
rad_sorted_ol = np.concatenate((rad_sorted_ol, rad_sorted_ol[:1]))
p_sorted_ol = np.concatenate((p_sorted_ol, p_sorted_ol[:1]))


file_path_cl = cl_data_path + times[0] + "/p_airfoil.raw"
data_cl = read_surface_data(file_path_cl)
rad_cl, theta_cl = compute_polar_coordinates(data_cl.x.values, data_cl.y.values, 0.2, 0.2)

theta_sorting_cl = np.argsort(theta_cl)
theta_sorted_cl = theta[theta_sorting_cl]
rad_sorted_cl = rad[theta_sorting_cl]
p_sorted_cl = data.p.values[theta_sorting_cl]
theta_sorted_cl = np.concatenate((theta_sorted_cl, theta_sorted_cl[:1]))
rad_sorted_cl = np.concatenate((rad_sorted_cl, rad_sorted_cl[:1]))
p_sorted_cl = np.concatenate((p_sorted_cl, p_sorted_cl[:1]))


# create initial plot
fig, ax = plt.subplots(1, 1, figsize=(5, 4), subplot_kw={'projection': 'polar'})
ln_cl, = ax.plot(theta_sorted_cl + np.pi, p_sorted_cl, color="r")
ln, = ax.plot(theta_sorted + np.pi, p_sorted, color="b", linestyle='--')
ln_ol, = ax.plot(theta_sorted_ol + np.pi, p_sorted_ol, color="g")

ax.grid(True)
ax.set_theta_zero_location("W")
ax.set_rlim(-2, 0)
ax.set_rticks(np.linspace(-1.4, 0, 5))
ax.set_xlabel(r"$p$")
ax.legend(loc='best', bbox_to_anchor=(1.05, 1.1))
ax.text(-0.01, -0.3, r"flow direction $\rightarrow$")
time_label = ax.text(-0.8, 0.7, r"$\tilde{t}=0.00$")

plt.savefig('results.png')


# update function for animation
def update(frame):
    file_path = data_path + frame + "/p_airfoil.raw"
    data = read_surface_data(file_path)
    p_sorted = data.p.values[theta_sorting]
    p_sorted = np.concatenate((p_sorted, p_sorted[:1]))
    ln.set_data(theta_sorted + np.pi, p_sorted)

    file_path = ol_data_path + frame + "/p_airfoil.raw"
    data = read_surface_data(file_path)
    p_sorted_ol = data.p.values[theta_sorting_ol]
    p_sorted_ol = np.concatenate((p_sorted_ol, p_sorted_ol[:1]))
    ln_ol.set_data(theta_sorted_ol + np.pi, p_sorted_ol)

    file_path = cl_data_path + frame + "/p_airfoil.raw"
    data = read_surface_data(file_path)
    p_sorted_cl = data.p.values[theta_sorting_cl]
    p_sorted_cl = np.concatenate((p_sorted_cl, p_sorted_cl[:1]))
    ln_cl.set_data(theta_sorted_cl + np.pi, p_sorted_cl)

    time_str = r"{:1.2f}$".format(float(frame))
    time_label.set_text(r"$\tilde{t}=" + time_str)
    print(frame)
    return ln,


ani = FuncAnimation(fig, update, frames=times[:800])

ani.save("surface_pressure.mp4", fps=25, extra_args=['-vcodec', 'libx264'])
