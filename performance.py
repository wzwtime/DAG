# coding=utf-8
import heft_new
import cpop_new
import os


def write(q, v, N):
    n = 1
    while n <= N:
        heft = heft_new.Heft(q, n, v)
        heft_makespan = heft.heft()
        min_costs = heft.min_costs

        cpop = cpop_new.Cpop(q, n, v)
        cpop_makespan = cpop.cpop()
        cp_min_costs = cpop.cp_min_costs

        slr_heft = round(1.0 * heft_makespan / cp_min_costs, 4)
        # slr_cpop = round(1.0 * cpop_makespan / cp_min_costs, 4)
        slr_cpop = cpop.slr

        # speedup_heft = round(1.0 * min_costs / heft_makespan, 4)
        speedup_heft = heft.speedup
        speedup_cpop = round(1.0 * min_costs / cpop_makespan, 4)

        running_time_heft = heft.running_time
        running_time_cpop = cpop.running_time
        # print("time", running_time_heft, running_time_cpop)

        def write_slr_speedup():
            """computing schedule length ratio"""
            file_path = "performance/v=" + str(v) + "/"
            filename = file_path + "slr_speedup_heft_cpop.txt"
            file_dir = os.path.split(filename)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            with open(filename, 'a') as file_object:
                info = str(v) + "  " + str(min_costs) + "  " + str(cp_min_costs) + "  " + str(
                    heft_makespan) + "  " \
                       + str(cpop_makespan) + "  " + str(slr_heft) + "  " + str(slr_cpop) + "  " + str(
                    speedup_heft) \
                       + "  " + str(speedup_cpop) + "  " + str(running_time_heft) + "  " + str(
                    running_time_cpop) + "\n"
                file_object.write(info)

        write_slr_speedup()

        print(slr_heft, slr_cpop, speedup_heft, speedup_cpop)
        n += 1

"""
def read(v, slr_name, speedup_name):
    """"""
    file_path = "performance/v=" + str(v) + "/"
    filename = file_path + "slr_speedup_heft_cpop.txt"
    with open(filename, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            line_list = line.split()
            v_ = int(line_list[0])
            if slr_name == SLR_heft and speedup_name == Speedup_heft:
                heft_slr_ = float(line_list[5])
                slr_name[v_].append(heft_slr_)
                speedup_heft_ = float(line_list[7])
                speedup_name[v_].append(speedup_heft_)

            elif slr_name == SLR_cpop and speedup_name == Speedup_cpop:
                cpop_slr_ = float(line_list[6])
                slr_name[v_].append(cpop_slr_)
                speedup_cpop_ = float(line_list[8])
                speedup_name[v_].append(speedup_cpop_)
"""

if __name__ == "__main__":
    q = 34
    v = 100
    N = 1
    write(q, v, N)
    # for v in range(40, 41, 20):
    #     for q in range(3, 4):
    #         write(q, v, N)



