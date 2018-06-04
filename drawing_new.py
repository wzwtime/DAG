import matplotlib.pyplot as plt

SLR_adts = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
SLR_heft = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
SLR_cpop = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
SLR_peft = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}

Speedup_adts = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
Speedup_heft = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
Speedup_cpop = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
Speedup_peft = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}

Time_adts = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
Time_heft = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
Time_cpop = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}
Time_peft = {
    20: [],
    40: [],
    60: [],
    80: [],
    100: [],
}

heft_info = []
cpop_info = []
peft_info = []
adts_info = []


def read_slr_speedup_time(slr_name, speedup_name, time_name, v):
    """read in slr file"""
    file_path = "performance/6_4/v=" + str(v) + "/"
    filename = file_path + "slr_speedup_heft_cpop.txt"
    with open(filename, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            # if line.startswith("#"):
            #     continue
            line_list = line.split()
            v_ = int(line_list[0])
            if slr_name == SLR_heft and speedup_name == Speedup_heft and time_name == Time_heft:
                heft_slr_ = float(line_list[7])
                slr_name[v_].append(heft_slr_)
                speedup_heft_ = float(line_list[10])
                speedup_name[v_].append(speedup_heft_)
                time_heft_ = int(line_list[13])
                time_name[v_].append(time_heft_)
            elif slr_name == SLR_cpop and speedup_name == Speedup_cpop and time_name == Time_cpop:
                cpop_slr_ = float(line_list[8])
                slr_name[v_].append(cpop_slr_)
                speedup_cpop_ = float(line_list[11])
                speedup_name[v_].append(speedup_cpop_)
                time_cpop_ = int(line_list[14])
                time_name[v_].append(time_cpop_)
            elif slr_name == SLR_peft and speedup_name == Speedup_peft and time_name == Time_peft:
                peft_slr_ = float(line_list[9])
                slr_name[v_].append(peft_slr_)
                speedup_peft_ = float(line_list[12])
                speedup_name[v_].append(speedup_peft_)
                time_peft_ = int(line_list[15])
                time_name[v_].append(time_peft_)


def read_slr_speedup_time_adts(slr_name, speedup_name, time_name, v):
    """read in slr file"""
    file_path = "performance/adts_v=" + str(v) + "/"
    filename = file_path + "slr_speedup_heft_cpop.txt"
    with open(filename, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            # if line.startswith("#"):
            #     continue
            line_list = line.split()
            v_ = int(line_list[0])
            if slr_name == SLR_adts and speedup_name == Speedup_adts and time_name == Time_adts:
                adts_slr_ = float(line_list[3])
                slr_name[v_].append(adts_slr_)
                speedup_adts_ = float(line_list[4])
                speedup_name[v_].append(speedup_adts_)
                time_adts_ = int(line_list[5])
                time_name[v_].append(time_adts_)


for v in range(20, 101, 20):
    read_slr_speedup_time(SLR_heft, Speedup_heft, Time_heft, v)
    read_slr_speedup_time(SLR_cpop, Speedup_cpop, Time_cpop, v)
    read_slr_speedup_time(SLR_peft, Speedup_peft, Time_peft, v)
    read_slr_speedup_time_adts(SLR_adts, Speedup_adts, Time_adts, v)

# print("SLR_heft=", SLR_heft)
# print("Speedup_heft=", Speedup_heft)
# print("Time_heft=", Time_heft)
#
#
# print("SLR_cpop=", SLR_cpop)
# print("speedup_cpop=", Speedup_cpop)
# print("Time_cpop =", Time_cpop)
#
# print("SLR_peft=", SLR_peft)
# print("speedup_peft=", Speedup_peft)
# print("Time_peft =", Time_peft)
#
# print("SLR_adts=", SLR_adts)
# print("speedup_adts=", Speedup_adts)
# print("Time_adts =", Time_adts)


# print(len(SLR_heft[20]))
# print(len(SLR_cpop[20]))
# print(len(SLR_peft[20]))
#
# print(len(SLR_heft[40]))
# print(len(SLR_cpop[40]))
# print(len(SLR_peft[40]))

# print(len(SLR_heft[60]))
# print(len(SLR_cpop[60]))
#
# print(len(SLR_heft[80]))
# print(len(SLR_cpop[80]))
#
# print(len(SLR_heft[100]))
# print(len(SLR_cpop[100]))

# print(len(SLR_adts[20]))
#
# print(len(SLR_adts[40]))
# print(len(SLR_adts[60]))
#
# print(len(SLR_adts[80]))
# print(len(SLR_adts[100]))


def avg_slr_speedup_time(list_, info):
    """computing avg slr"""
    for key, values in list_.items():
        # print(key, values)
        temp_info = []
        min_info = min(values)
        temp_info.append(min_info)
        max_info = max(values)
        temp_info.append(max_info)
        avg_ = round(sum(values) / len(values), 3)
        temp_info.append(avg_)
        info.append(temp_info)


def get_avg_slr_speedup_time(txt, heft, cpop, peft, adts):
    avg_slr_speedup_time(heft, heft_info)
    print("heft-avg_" + str(txt) + "=", heft_info)

    avg_slr_speedup_time(cpop, cpop_info)
    print("cpop-avg_" + str(txt) + "=", cpop_info)

    avg_slr_speedup_time(peft, peft_info)
    print("peft-avg_" + str(txt) + "=", peft_info)

    avg_slr_speedup_time(adts, adts_info)
    print("adts-avg_" + str(txt) + "=", adts_info)


def drawing(ylabel):
    """"""
    input_values = list(range(20, 101, 20))   # the number of tasks
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # plt.title("Average Job Slowdown of different scheduling algorithms.")
    plt.xlabel("Number of Nodes", fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    # my_x_ticks = range(20, 101, 20)
    # plt.xticks(my_x_ticks)

    # plt.xlim(0, int(length) + 1)
    # plt.ylim(2, 5)
    y1_value = []
    y2_value = []
    y3_value = []
    y4_value = []
    for i in range(len(heft_info)):
        y1_value.append(heft_info[i][2])
    for i in range(len(cpop_info)):
        y2_value.append(cpop_info[i][2])
    for i in range(len(peft_info)):
        y3_value.append(peft_info[i][2])
    for i in range(len(adts_info)):
        y4_value.append(adts_info[i][2])
    plt.plot(input_values, y1_value, "^-.", label="HEFT")
    plt.plot(input_values, y2_value, "8--", label="CPOP")
    plt.plot(input_values, y3_value, "s--", label="PEFT")
    plt.plot(input_values, y4_value, "d--", label="ADTS")

    # plt.grid(True)         # 显示网格
    plt.legend(loc='upper left')           # 显示图例
    # plt.savefig('asd.png', bbox_inches='tight')
    # plt.close()
    plt.show()


# txt = "slr"
# get_avg_slr_speedup_time(txt, SLR_heft, SLR_cpop, SLR_peft, SLR_adts)
# ylabel = "Average SLR"


# txt = "speedup"
# get_avg_slr_speedup_time(txt, Speedup_heft, Speedup_cpop, Speedup_peft, Speedup_adts)
# ylabel = "Average Speedup"

# txt = "time"
# get_avg_slr_speedup_time(txt, Time_heft, Time_cpop, Time_peft, Time_adts)
# ylabel = "Average Running Time(ms)"
#
# drawing(ylabel)


def box(name_, ylabel_, list_):

    plt.title(name_)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel("Number of Nodes", fontsize=12)
    plt.ylabel(ylabel_, fontsize=12)
    plt.boxplot(tuple(list_.values()), labels=SLR_heft.keys())
    plt.show()


def get_box(y_label, heft, cpop, peft, adts):
    name = "HEFT"
    box(name, y_label, heft)

    name = "CPOP"
    box(name, y_label, cpop)

    name = "PEFT"
    box(name, y_label, peft)

    name = "ADTS"
    box(name, y_label, adts)


# ylabel = "Schedule Length Ratio"
# get_box(ylabel, SLR_heft, SLR_cpop, SLR_peft, SLR_adts)
#
# ylabel = "Speedup"
# get_box(ylabel, Speedup_heft, Speedup_cpop, Speedup_peft, Speedup_adts)
#
# ylabel = "Running Time(ms)"
# get_box(ylabel, Time_heft, Time_cpop, Time_peft, Time_adts)


slr_ccr_heft = {
    0.1: [],
    0.5: [],
    1.0: [],
    5.0: [],
    10.0: [],
}
slr_ccr_cpop = {
    0.1: [],
    0.5: [],
    1.0: [],
    5.0: [],
    10.0: [],
}


def read_slr_ccr(slr_ccr_name):
    """read in slr_ccr_name file"""
    filename = "ccr.txt"
    with open(filename, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            line_list = line.split()
            ccr_ = float(line_list[0])
            if slr_ccr_name == slr_ccr_heft:
                heft_slr_ = float(line_list[5])
                slr_ccr_name[ccr_].append(heft_slr_)
            elif slr_ccr_name == slr_ccr_cpop:
                cpop_slr_ = float(line_list[6])
                slr_ccr_name[ccr_].append(cpop_slr_)


# read_slr_ccr(slr_ccr_heft)
#
# print("heft-slr_ccr=", slr_ccr_heft)
# read_slr_ccr(slr_ccr_cpop)
#
# print("cpop-slr_ccr=", slr_ccr_cpop)


"""slr_ccr_box"""
"""
plt.title("HEFT")
plt.xlabel("CCR", fontsize=11)
plt.ylabel("Schedule Length Ratio", fontsize=11)
plt.boxplot(tuple(slr_ccr_heft.values()), labels=slr_ccr_cpop.keys())
plt.show()

"""
avg_slr_ccr_heft = []
avg_slr_ccr_cpop = []


def avg_slr_ccr(slr_ccr_name, info):
    """computing avg slr_ccr"""
    for key, values in slr_ccr_name.items():
        # print(key, values)
        avg_slr_ = round(sum(values) / len(values), 2)
        info.append(avg_slr_)


# avg_slr_ccr(slr_ccr_heft, avg_slr_ccr_heft)
# print("heft-avg_slr_ccr=", avg_slr_ccr_heft)
# avg_slr_ccr(slr_ccr_cpop, avg_slr_ccr_cpop)
# print("cpop-avg_slr_ccr=", avg_slr_ccr_cpop)
#

def drawing_avg_slr_ccr():
    """绘制折线图"""
    input_values = (1, 2, 3, 4, 5)  # 任务数量
    # input_values = (0.1, 0.5, 1.0, 5.0, 10.0)  # 任务数量
    # plt.title("Average Job Slowdown of different scheduling algorithms.")
    plt.xlabel("CCR", fontsize=11)
    plt.ylabel("Average SLR", fontsize=11)
    # my_x_ticks = range(20, 101, 20)
    # plt.xticks(my_x_ticks)

    # plt.xlim(0, int(length) + 1)
    # plt.ylim(2, 5)
    y1_value = tuple(avg_slr_ccr_heft)
    y2_value = tuple(avg_slr_ccr_cpop)

    plt.plot(input_values, y1_value, "^-.", label="HEFT")
    plt.plot(input_values, y2_value, "8--", label="CPOP")

    # plt.grid(True)         # 显示网格
    plt.legend(loc='upper left')           # 显示图例
    # plt.savefig('asd.png', bbox_inches='tight')
    # plt.close()
    plt.show()


# drawing_avg_slr_ccr()


slr_beta_heft = {
    0.1: [],
    0.25: [],
    0.5: [],
    0.75: [],
    1.0: [],
}
slr_beta_cpop = {
    0.1: [],
    0.25: [],
    0.5: [],
    0.75: [],
    1.0: [],
}


def read_slr_beta(slr_beta_name):
    """read in slr_ccr_name file"""
    filename = "slr_beta.txt"
    with open(filename, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            line_list = line.split()
            beta_ = float(line_list[0])
            if slr_beta_name == slr_beta_heft:
                heft_slr_ = float(line_list[5])
                slr_beta_name[beta_].append(heft_slr_)
            elif slr_beta_name == slr_beta_cpop:
                cpop_slr_ = float(line_list[6])
                slr_beta_name[beta_].append(cpop_slr_)

#
# read_slr_beta(slr_beta_heft)
# print("heft=", slr_beta_heft)
#
# read_slr_beta(slr_beta_cpop)
# print("cpop=", slr_beta_cpop)

"""slr_beta_box"""

"""
plt.title("CPOP")
plt.xlabel("Beta", fontsize=11)
plt.ylabel("Schedule Length Ratio", fontsize=11)
plt.boxplot(tuple(slr_beta_cpop.values()), labels=slr_beta_cpop.keys())
plt.show()
"""

avg_slr_beta_heft = []
avg_slr_beta_cpop = []


def avg_slr_beta(slr_beta_name, info):
    """computing avg slr_beta"""
    for key, values in slr_beta_name.items():
        # print(key, values)
        avg_slr_ = round(sum(values) / len(values), 2)
        info.append(avg_slr_)


# avg_slr_beta(slr_beta_heft, avg_slr_beta_heft)
# print("heft-avg_slr_beta=", avg_slr_beta_heft)
# avg_slr_beta(slr_beta_cpop, avg_slr_beta_cpop)
# print("cpop-avg_slr_beta=", avg_slr_beta_cpop)


def drawing_avg_slr_beta():
    """绘制折线图"""
    # input_values = (0.1, 0.5, 1.0, 5.0, 10.0)  # 任务数量
    input_values = (0.1, 0.25, 0.50, 0.75, 1.0)  # 任务数量
    # plt.title("Average Job Slowdown of different scheduling algorithms.")
    plt.xlabel("BETA", fontsize=11)
    plt.ylabel("Average SLR", fontsize=11)
    # my_x_ticks = range(20, 101, 20)
    # plt.xticks(my_x_ticks)

    # plt.xlim(0, int(length) + 1)
    # plt.ylim(2, 5)
    y1_value = tuple(avg_slr_beta_heft)
    y2_value = tuple(avg_slr_beta_cpop)

    plt.plot(input_values, y1_value, "^-.", label="HEFT")
    plt.plot(input_values, y2_value, "8--", label="CPOP")

    # plt.grid(True)         # 显示网格
    plt.legend(loc='best')           # 显示图例
    # plt.savefig('asd.png', bbox_inches='tight')
    # plt.close()
    plt.show()


# drawing_avg_slr_beta()
