import numpy as np
import matplotlib.pyplot as plt
n_groups = 5

# heft = (2.05, 1.93, 2.11, 3.98, 6.11)
# cpop = (2.52, 2.23, 2.42, 4.18, 6.12)

# slr
# # 一位小数
# heft = (3.0, 3.3, 3.7, 3.7, 3.9)
# cpop = (3.2, 3.4, 3.8, 3.8, 4.1)

# # 2位小数
# heft = (3.0, 3.33, 3.74, 3.7, 3.94)
# cpop = (3.22, 3.44, 3.84, 3.8, 4.09)

# # 3位小数
# heft = (2.996, 3.326, 3.744, 3.704, 3.939)
# cpop = (3.215, 3.441, 3.839, 3.803, 4.092)

# 4位小数
# heft = (2.9964, 3.3262, 3.7436, 3.7042, 3.9389)
# cpop = (3.2151, 3.4407, 3.8388, 3.8029, 4.092)
# rein = (3.2151, 3.4407, 3.8388, 3.8029, 4.092)

# speedup
# heft = (1.61, 2.07, 2.14, 2.23, 2.31)
# cpop = (1.56, 1.82, 1.85, 1.98, 1.97)


heft = (0.879, 1.026, 1.156, 1.229, 1.304)
cpop = (0.886, 1.1, 1.229, 1.409, 1.351)
rein = (1.087, 1.208, 1.325, 1.407, 1.458)
# beta
# heft = [3.95, 2.99, 2.71, 2.56, 3.16]
# cpop = [3.8, 3.23, 2.93, 2.63, 3.62]

fig, ax = plt.subplots()

index = np.arange(n_groups)
# bar_width = 0.35
bar_width = 0.25

opacity = 0.8
# color=(0, 0, 0),
# color=(0.25, 0.25, 0.25),
# color=(0.5, 0.5, 0.5),
rects1 = ax.bar(index, heft, bar_width,
                alpha=opacity, color=(0, 0, 0),
                label='HEFT')

rects2 = ax.bar(index + bar_width, cpop, bar_width,
                alpha=opacity, color=(0.4, 0.4, 0.4),
                label='CPOP')
rects3 = ax.bar(index + bar_width + bar_width, rein, bar_width,
                alpha=opacity, color=(0.8, 0.8, 0.8),
                label='ADTS')

# ax.set_xlabel('BETA')
ax.set_xlabel('Number of Nodes', fontsize=11)
ax.set_ylabel('Average Speedup', fontsize=11)
# ax.set_title('Scores by group and gender')
# ax.set_xticks(index + bar_width / 2)
ax.set_xticks(index + bar_width )

# ax.set_xticklabels(('0.1', '0.25', '0.5', '0.75', '1.0'))
ax.set_xticklabels(('20', '40', '60', '80', '100'),)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
ax.legend()

fig.tight_layout()
plt.show()
