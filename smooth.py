import numpy as np
import matplotlib.pyplot as plt


makespans = []
f_path = "makespan/v=" + str(20) + "n=" + str(34) + "/"
filename = f_path + "makespan.txt"
with open(filename, 'r') as file_object:
    lines = file_object.readlines()
    # print(len(lines))
    heft = int(lines[0])
    # print(heft)
    for i in range(1, len(lines)):
        makespan = int(lines[i])
        makespans.append(makespan)

sp = makespans
N = 35
n = np.ones(N)
weights = n / N
sma = np.convolve(weights, sp)[N-1:-N+1]

t = np.arange(N-1, len(sp))
# plot(t,sp[N-1:],lw=1)
# plot.axhline(heft, linewidth=0.5, color='r')

plt.axhline(heft, linewidth=1.5, color='r', label="HEFT")

plt.xlabel("Episode", fontsize=12)
plt.ylabel("- Makespan", fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.plot(t, sma, color='b', label="ADTS")
plt.legend(loc='best')
# plt.ylim(-325, -125)
plt.show()
