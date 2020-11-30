from sklearn.kernel_ridge import KernelRidge
import numpy as np
import matplotlib.pyplot as plt
import pickle

A = []
f = []
c_d = []
c_l = []
c_d_max = []
c_d_min = []
c_l_max = []
c_l_min = []
with open(r"data_py.config", "rb") as file:
    data = pickle.load(file)

tml = (np.abs(list(data.values())[0][0] - 4.0)).argmin()

for key in data.keys():
    first, sec = key.split("-")
    A.append(float(first[1:]))
    f.append(float(sec[1:]))
    c_d.append(np.mean(data[key][1][tml:]))
    c_l.append(np.mean(data[key][2][tml:]))
    c_d_max.append(np.max(data[key][1][tml:]))
    c_d_min.append(np.min(data[key][1][tml:]))
    c_l_max.append(np.max(data[key][2][tml:]))
    c_l_min.append(np.min(data[key][2][tml:]))
A = np.asarray(A)
f = np.asarray(f)
c_d = np.asarray(c_d)
c_l = np.asarray(c_l)
c_d_max = np.asarray(c_d_max)
c_d_min = np.asarray(c_d_min)
c_l_max = np.asarray(c_l_max)
c_l_min = np.asarray(c_l_min)


def plot_data(arg1, arg2, arg3, lim):
    fig, (ax1) = plt.subplots(1, 1, figsize=(7, 7))
    levels = np.linspace(lim[0], lim[1], 200)
    levels_line = np.linspace(lim[0], lim[1], 50)
    cntr2 = ax1.tricontourf(arg1, arg2, arg3, levels=levels, cmap="jet")
    ax1.tricontour(arg1, arg2, arg3, levels=levels_line)
    ax1.scatter(arg1, arg2, s=1, color='k')
    ax1.set_ylabel(r"$S_f \times 10$")
    ax1.set_xlabel(r"$\Omega$")
    fig.colorbar(cntr2, ax=ax1)
    plt.subplots_adjust(hspace=0.5)


w = [1, 1]  # need to update
fn_1 = w[0] * ((c_d ** 2 + c_l ** 2) ** .5) + w[1] * (((c_d_max - c_d_min) ** 2 + (c_l_max - c_l_min) ** 2) ** .5)

X = np.asarray((A, f)).transpose()

# krr
krr = KernelRidge(alpha=1e-7, kernel='rbf', gamma=2).fit(X, fn_1)
loss = np.sum((krr.predict(X) - fn_1) ** 2)

# data setting for prediction
x = np.arange(0.1, 3.5, 0.3)
y = np.arange(3, 15.1, 1)
xx, yy = np.meshgrid(x, y)
A_new = xx.reshape(-1, 1)
f_new = yy.reshape(-1, 1)
data = np.asarray([A_new[:, 0], f_new[:, 0]]).transpose()
re = krr.predict(data)

# plot
lim = [3, 9]
plot_data(A, f, fn_1, lim)

# krr plot
plot_data(A_new[:, 0], f_new[:, 0], re, lim)
