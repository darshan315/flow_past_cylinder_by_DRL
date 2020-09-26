import numpy as np
import matplotlib.pyplot as plt

filename = "postProcessing/forces/0/coefficient.dat"

data = np.loadtxt(filename, unpack=True, usecols=[0, 1, 3])
data = data[:, 6000:]

Data = np.column_stack((data[0], data[1], data[2]))
np.savetxt('postProcessing/filtered_data.dat', Data, fmt='%.6e', delimiter='   ', newline='\n', header='Timestep     Cd             Cl\n', footer='')

mean_cd = np.mean(data[1])
std_cd = np.std(data[1])

mean_cl = np.mean(data[2])
std_cl = np.std(data[2])

text_file = open("postProcessing/mean_std.txt", "w")
text_file.write("Mean Value(Cd)         : %s\n" % mean_cd)
text_file.write("Standard deviation(Cd) : %s" % std_cd)
text_file.write("\n\n")
text_file.write("Mean Value(Cl)         : %s\n" % mean_cl)
text_file.write("Standard deviation(Cl) : %s" % std_cl)
text_file.close()

plt.plot(data[0], data[1], linewidth=2)
plt.xlabel('time(s)')
plt.ylabel('Cd')
plt.title('Values of Cd after 3 s')
plt.savefig('postProcessing/Cd.png')
plt.close()
plt.plot(data[0], data[2], linewidth=2)
plt.xlabel('time(s)')
plt.ylabel('Cd')
plt.title('Values of Cd after 3 s')
plt.savefig('postProcessing/Cl.png')
plt.close()
