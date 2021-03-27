from sklearn.kernel_ridge import KernelRidge
import numpy as np
import matplotlib.pyplot as plt
import pickle
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 160
mpl.rc('text', usetex=True)
plt.rcParams.update({'font.size': 7})

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

# uncontrolled state
cd_uc = [3.14741, 3.17212, 3.19653] # [cd_min, cd_mean, cd_max]
cl_uc = [-0.904919, -0.0126599, 0.878955] # [cl_min, cl_mean, cl_max]
uc_val = ((cd_uc[1]**2+cl_uc[1]**2)**.5) + (((cd_uc[2]-cd_uc[0])**2+(cl_uc[2]-cl_uc[0])**2)**.5)


def plot_data(arg1, arg2, arg3, lim, nointep):
    fig, (ax1) = plt.subplots(1, 1, figsize=(7, 7))
    levels = np.linspace(lim[0], lim[1], 200)
    levels_line = np.linspace(lim[0], lim[1], 30)
    if nointep:
        cntr2 = ax1.contourf(arg1, arg2, arg3, levels=levels, cmap="jet")
        ax1.contour(arg1, arg2, arg3, levels=levels_line, linewidths=1)
    else:
        cntr2 = ax1.tricontourf(arg1, arg2, arg3, levels=levels, cmap="jet")
        ax1.tricontour(arg1, arg2, arg3, levels=levels_line, linewidths=1)
    ax1.scatter(arg1, arg2, s=1, color='k')
    ax1.set_ylabel(r"$S_f \times 10$", fontsize=12)
    ax1.set_xlabel(r"$\Omega$", fontsize=12)
    ax1.tick_params(labelsize=12)
    ax1.set_ylim(4.8,14)
    cbar=fig.colorbar(cntr2, ax=ax1)
    cbar.ax.tick_params(labelsize=12)
    cbar.ax.set_ylabel(r"$\Phi$", fontsize=14)
    plt.subplots_adjust(hspace=0.5)


w = [1, 1]
fn_1 = (w[0]*((c_d**2+c_l**2)**.5)+w[1]*(((c_d_max-c_d_min)**2+(c_l_max-c_l_min)**2)**.5)) / uc_val

X = np.asarray((A, f)).transpose()

# krr
krr = KernelRidge(alpha=1e-7, kernel='rbf', gamma=1.5).fit(X, fn_1)
loss = np.sum((krr.predict(X) - fn_1) ** 2)

# uniform data setting for prediction
x = np.arange(0.1, 3.5, 0.1)
y = np.arange(3, 15.1, 0.3)
xx, yy = np.meshgrid(x, y)
A_new = xx.reshape(-1, 1)
f_new = yy.reshape(-1, 1)
data = np.asarray([A_new[:, 0], f_new[:, 0]]).transpose()
pred_uni = krr.predict(data)
rr = np.reshape(pred_uni, xx.shape)


# original plot on LHS data
lim = [0.5, 1.7]
plot_data(A, f, fn_1, lim, nointep=False)
plt.title("Original LHS Data")
plt.savefig('origin_plot_lhs.png')

# krr plot on LHS
plot_data(A,f, krr.predict(X), lim, nointep=False)
plt.title("Pridicted LHS Data")
plt.savefig('krr_lhs.png')

# error
lim_e = [0, 0.2]
plot_data(A, f, np.abs(fn_1 - krr.predict(X)), lim_e, nointep=False)
plt.title("Error between original and predicted LHS data")
plt.savefig('error.png')

# krr plot new uniform data
plot_data(xx, yy, rr, lim, nointep=True)
plt.title("Generalization on uniform Data")
plt.savefig('frr_for_new.png')
