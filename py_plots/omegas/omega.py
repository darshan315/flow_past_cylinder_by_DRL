#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import pickle
import matplotlib as mpl

import scipy.optimize
from scipy import fftpack


mpl.rcParams['figure.dpi'] = 160
mpl.rc('text', usetex=True)

# read trajectory data
## number of cell faces forming the cylinder patch
n_faces = 54
names = ["t", "omega", "omega_mean", "omega_log_std", "log_p", "entropy", "theta_sum", "dt_theta_sum"]
p_names = ["p{:d}".format(i) for i in range(n_faces)]

trajectory = pd.read_csv("trajectory.csv", sep=",", names=names + p_names, header=0)

tc = trajectory.t.values
omega = trajectory.omega.values
print("Shape of log_p: ", omega.shape)

tt = np.arange(0, 8, 0.01);
# a sin(2 pi f t)
omega_ol = 2.294 * np.sin(2 * np.pi * 7.128 * tt)

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(tt, omega_ol, "--", linewidth=1.2, markevery=70, label="open-loop controlled")

ax.plot(tc, omega, "-", linewidth=1.2, markevery=70, label="closed-loop controlled by DRL")

ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

ax.set_xlim((0, 8))
#ax.set_ylim((2.965, 3.26))
ax.set_ylabel(r"$\omega$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('omegas.png')

ol = np.mean(omega_ol)
cl = np.mean(omega)

print(f"ol = {ol}")
print(f"cl = {cl}")

a_ol = np.max(omega_ol) - np.min(omega_ol)
a_cl = np.max(omega[-100:]) - np.min(omega[-100:])

print(f"a_ol = {a_ol}")
print(f"a_cl = {a_cl}")

#################################################

# Theta


r = np.zeros(shape=(omega.shape[0]+1))
q = np.zeros(shape=omega.shape)

o_r = np.zeros(shape=(omega_ol.shape[0]+1))
o_q = np.zeros(shape=omega_ol.shape)

d_t = tc[281] - tc[280]
d_t_o = tt[2] - tt[1]


for i in range(len(tc)):
    q[i] = r[i] + omega[i] * 0.5 * d_t
    r[i+1] = q[i]

for i in range(len(tt)):
    o_q[i] = o_r[i] + omega_ol[i] * 0.5 * d_t_o
    o_r[i+1] = o_q[i]

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(tt, o_q, "-", linewidth=1.2, markevery=70, label=r"open-loop control")
ax.plot(tc, q, "--", linewidth=1.2, markevery=70, label=r"closed-loop control")
ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

ax.set_xlim((0, 8))
ax.set_ylabel(r"$\theta$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('inte_omegas.png')




############################
# sine curve fit
def fit_sin(tt, yy):
    """Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq",
    "period" and "fitfunc" """
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1] - tt[0]))  # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:]) + 1])  # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2. ** 0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2. * np.pi * guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w * t + p) + c

    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w / (2. * np.pi)
    fitfunc = lambda t: A * np.sin(w * t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1. / f, "fitfunc": fitfunc,
            "maxcov": np.max(pcov), "rawres": (guess, popt, pcov)}


# sine curve fitting

x_test = np.arange(5, 8, 0.01)
y_test = 0.6 + 0.5 * np.sin(9.2 * x_test + 0.5)

x = tc[281:]
yn = omega[281:]

res = fit_sin(x, yn)
print("Amplitude=%(amp)s, Angular freq.=%(omega)s, ordinary freq.=%(freq)s, phase=%(phase)s, offset=%(offset)s, "
      "Max. Cov.=%(maxcov)s" % res)

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(x, yn, "-", linewidth=1.2, markevery=70, label=r"original")
ax.plot(x, res["fitfunc"](x), "--", linewidth=1.2, markevery=70, label=r"regression")
# ax.axvline(x=2.19, color='k', linestyle='--', label='control starts for DRL')

# ax.set_xlim((0, 8))
ax.set_ylabel(r"$\omega$", fontsize=12)
ax.set_xlabel(r"$\tilde t$", fontsize=12)
ax.tick_params(labelsize=12)
ax.legend(loc='best', fontsize=12)

plt.savefig('reg_omegas.png')
