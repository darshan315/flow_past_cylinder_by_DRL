import numpy as np
import matplotlib.pyplot as plt

filename = "./forces/0/coefficient.dat"

data = np.loadtxt(filename, unpack=True, usecols=[0, 1])
data = data[:, 6000:]

plt.plot(data[0], data[1], linewidth=2)

mean_cd = np.mean(data[1])
std_cd = np.std(data[1])
Data = np.column_stack((data[0], data[1]))
np.savetxt('filtered_data.dat', Data, fmt='%.6e', delimiter='   ', newline='\n', header='Timestep     Cd\n', footer='')

text_file = open("mean_std.txt", "w")
text_file.write("Mean Value         : %s\n" % mean_cd)
text_file.write("Standard deviation : %s" % std_cd)
text_file.close()
