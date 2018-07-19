# coding=utf-8
import heft_new
import cpop_new
import peft
import time
import os
import mpq_ga


def write(q, v, N, nn):
    n = 1
    while n <= N:
        heft = heft_new.Heft(q, n, v, 0)
        heft_makespan = heft.heft()
        min_costs = heft.min_costs
        """Speedup-HEFT"""
        speedup_heft = heft.speedup

        cpop = cpop_new.Cpop(q, n, v)
        cpop_makespan = cpop.cpop()
        cp_min_costs = cpop.cp_min_costs

        peft_ = peft.Peft(v, q, n)
        peft_makespan = peft_.peft()

        PopSize = v
        g = 0
        mpq_ga_ = mpq_ga.MPQGA(PopSize)
        ga_makespan = mpq_ga_.mpqga(v, q, n, g)

        """slr"""
        slr_heft = round(1.0 * heft_makespan / cp_min_costs, 4)
        slr_cpop = cpop.slr
        slr_peft = round(1.0 * peft_makespan / cp_min_costs, 4)
        slr_ga = round(1.0 * ga_makespan / cp_min_costs, 4)

        """Speedup"""

        print("+++++++++speedup_heft= ", speedup_heft)
        speedup_cpop = round(1.0 * min_costs / cpop_makespan, 4)
        speedup_peft = round(1.0 * min_costs / peft_makespan, 4)
        speedup_ga = round(1.0 * min_costs / ga_makespan, 4)

        """Running Time"""
        time_heft = heft.running_time
        time_cpop = cpop.running_time
        time_peft = peft_.running_time
        time_ga = mpq_ga_.running_time
        # print("time", running_time_heft, running_time_cpop)

        def write_slr_speedup_time(nn):
            """computing schedule length ratio"""
            # mon = time.localtime(time.time())[1]
            # day = time.localtime(time.time())[2]
            mon = 7
            day = 18

            file_path = "performance/" + str(mon) + "_" + str(day) + "/v=" + str(v) + "_PopSize=" + \
                        str(int(PopSize/nn)) + "/"
            filename = file_path + "slr_speedup_heft_cpop.txt"
            file_dir = os.path.split(filename)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            with open(filename, 'a') as file_object:
                info = str(v) + "  " + str(q) + "  " + str(min_costs) + "  " + str(cp_min_costs) + "  " \
                       + str(heft_makespan) + "  " + str(cpop_makespan) + "  " + str(peft_makespan) + "  " \
                       + str(slr_heft) + "  " + str(slr_cpop) + "  " + str(slr_peft) + "  " + str(speedup_heft) + "  " \
                       + str(speedup_cpop) + "  " + str(speedup_peft) + "  " + str(time_heft) + "  " + str(time_cpop) \
                       + "  " + str(time_peft) + "  " + str(ga_makespan) + "  " + str(slr_ga) + "  " + str(speedup_ga) \
                       + "  " + str(time_ga) + "\n"
                file_object.write(info)

        write_slr_speedup_time(nn)
        print("---------------------", n)
        print("slr =", slr_heft, slr_cpop, slr_peft, slr_ga)
        print("speedup =", speedup_heft, speedup_cpop, speedup_peft, speedup_ga)
        print("time =", time_heft, time_cpop, time_peft, time_ga)
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
    q = 4
    v = 20
    N = 1
    write(q, v, N, 1)
    qvn = [[36, 40, 35, 39, 34], [20, 14, 18, 15, 17], [14, 7, 5, 2, 5], [6, 3, 3, 0, 1], [3, 1, 1, 1, 1]]

    # for v in range(20, 101, 20):
    #     for q in range(3, 8):
    #         i = int(v / 20) - 1
    #         j = q - 3
    #         if not (v == 80 and q == 6):
    #             N = qvn[i][j]
    #             write(q, v, N, 2)
