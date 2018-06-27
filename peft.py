# coding=utf-8
import operator
import copy
import time
import heft_new


class Peft:

    def __init__(self, v_, q_, n_):
        """n is which dag"""
        self.heft = heft_new.Heft(q_, n_, v_)
        self.pred = self.heft.pred_list()
        self.pred.sort(key=operator.itemgetter(0), reverse=False)
        self.computation_costs = self.heft.computation_costs
        self.dag = self.heft.dag
        # self.dag = {}
        # self.computation_costs = []
        self.v = v_
        self.q = q_
        self.n = n_
        self.M = 10000
        # self.pred = []
        self.oct_table = {}
        self.rank_oct = []
        self.rank_oct_copy = []
        self.ready_list = []
        self.Pi = {}
        self.scheduler = []
        self.makespan = 0
        self.start_time = 0
        self.end_time = 0
        self.running_time = 0
        self.Tlevel = []

    def read_dag(self):
        """q is the number of processors, n is which graph"""
        filename = 'save_dag/new/v=' + str(self.v) + 'q=' + str(self.q) + '\_' + str(self.n) + '_dag_q=' \
                   + str(self.q) + '.txt'
        with open(filename, 'r') as file_object_:
            lines = file_object_.readlines()
            task_id = 0
            for line in lines:
                line_list = line.split()
                task_id = int(line_list[0])
                succ_dict = {}
                for line_ in lines:
                    line_list_ = line_.split()
                    task_id_ = int(line_list_[0])
                    succ_id_ = int(line_list_[1])
                    succ_weight = int(line_list_[2])
                    if task_id == task_id_:
                        succ_dict[succ_id_] = succ_weight
                self.dag[task_id] = succ_dict
            self.dag[task_id + 1] = {}
        return self.dag

    def read_computation_costs(self):
        """q is the number of processors, n is which graph"""
        filename = 'save_dag/new/v=' + str(self.v) + 'q=' + str(self.q) + '\_' + str(self.n) \
                   + '_computation_costs_q=' + str(self.q) + '.txt'
        with open(filename, 'r') as file_object:
            lines = file_object.readlines()
            for line in lines:
                line_list = line.split()
                temp_list = []
                for i in range(len(line_list)):
                    temp_list.append(int(line_list[i]))
                self.computation_costs.append(temp_list)
        return self.computation_costs

    def get_pred(self):
        """"""
        # self.read_dag()
        for job in range(1, self.v + 1):
            temp = []
            for j in range(self.v):
                if job in self.dag[j + 1].keys():
                    sub_pred = j + 1
                    temp.append(sub_pred)
            self.pred.append([job, temp])
        return self.pred

    def other_nodes(self, ti):
        """"""
        oct_table = []
        for pk in range(1, self.q + 1):
            # print("parent and it's processor=", ti, pk)
            max_oct = 0
            for tj in self.dag[ti].keys():
                """tj is succ of ti"""
                # print("child", tj)
                min_oct = self.M
                for pw in range(1, self.q + 1):
                    # print("child processor=", pw)
                    """find OCT(tj, pw)"""
                    oct_tj_pw = self.oct_table[tj][pw - 1]
                    # print("OCT(tj, pw)=", oct_tj_pw)
                    """find w(tj, pw)"""
                    w_tj_pw = self.computation_costs[tj - 1][pw - 1]
                    # print("w(tj, pw)=", w_tj_pw)
                    """find avg_ci,j"""
                    if pw == pk:
                        avg_cij = 0
                    else:
                        avg_cij = self.dag[ti][tj]
                        # print("avg_cij=", avg_cij)
                    sum_oct = oct_tj_pw + w_tj_pw + avg_cij
                    if min_oct > sum_oct:
                        min_oct = sum_oct
                if max_oct < min_oct:
                    max_oct = min_oct
            oct_table.append(max_oct)

        self.oct_table[ti] = oct_table
        avg_oct = round(sum(oct_table) / self.q, 1)
        self.rank_oct.append([ti, avg_oct])

    def get_oct_table_and_rank_oct(self):
        """compute OCT table and rank_oct"""
        # self.read_dag()
        # self.get_pred()
        # self.read_computation_costs()
        ti = self.v
        while ti > 0:
            if len(self.dag[ti]) == 0:
                self.oct_table[ti] = list([i - i for i in range(self.q)])
                self.rank_oct.append([ti, 0])
            else:
                """other nodes"""
                self.other_nodes(ti)
            ti -= 1
            self.rank_oct.sort(key=operator.itemgetter(1), reverse=True)
            self.rank_oct_copy = copy.deepcopy(self.rank_oct)
        return self.oct_table, self.rank_oct

    def add_pi(self, pi_, job_, est_, eft_):
        """Join the task to the list and add the task to the schedule list"""
        list_pi = []
        if pi_ in self.Pi.keys():
            list_pi = list(self.Pi[pi_])
            list_pi.append({'job': job_, 'est': est_, 'end': eft_})
            self.Pi[pi_] = list_pi
            self.scheduler.append([job_, pi_])
        else:
            list_pi.append({'job': job_, 'est': est_, 'end': eft_})
            self.Pi[pi_] = list_pi
            self.scheduler.append([job_, pi_])
        if job_ == self.v:
            self.makespan = eft_
        self.Tlevel.append(job_)

    def sched_entry_task(self, job):
        """entry task"""
        label_pi = 0
        label_est = 0
        label_eft = 0
        min_o_eft = self.M
        for pi in range(self.q):
            eft = self.computation_costs[job - 1][pi]
            oct_ = self.oct_table[job][pi]
            o_eft = eft + oct_
            if min_o_eft > o_eft:
                min_o_eft = o_eft
                label_pi = pi + 1
                label_eft = self.computation_costs[job - 1][label_pi - 1]
        self.add_pi(label_pi, job, label_est, label_eft)
        """update ready_list"""
        num_succ = len(self.dag[job].keys())
        for i in range(num_succ):
            succ = self.rank_oct.pop(0)[0]
            self.ready_list.append(succ)

    def get_aft(self, job_pred_j):
        """"""
        aft = 0
        pred_pi = 0
        for k in range(self.v):
            if job_pred_j == self.rank_oct_copy[k][0]:
                # print(self.scheduler[k][1])
                pred_pi = self.scheduler[k][1]          # self.scheduler[k][1] is 1  !!!!!! 6.2
                aft = 0
                for m in range(len(self.Pi[pred_pi])):
                    if self.Pi[pred_pi][m]['job'] == job_pred_j:
                        aft = self.Pi[pred_pi][m]['end']
        return aft, pred_pi

    def pred_max_nm(self, pi_, job_pred_, job_):
        """The maximum time spent on a pred node."""
        max_nm_ = 0
        for j in range(len(job_pred_)):
            job_pred_j = job_pred_[j]
            """get aft"""
            aft, pred_pi = self.get_aft(job_pred_j)

            # computing cmi
            if pi_ == pred_pi:
                cmi = 0
            else:
                cmi = self.dag[job_pred_[j]][job_]
            if max_nm_ < aft + cmi:
                max_nm_ = aft + cmi
        return max_nm_

    def update_ready_list(self):
        """update ready_list"""

        if self.rank_oct:
            candidate_job = self.rank_oct[0][0]
            # print("candidate_job =", candidate_job)
            """Judge whether the pred are all complete scheduled ?"""
            num_pred = len(self.pred[candidate_job - 1][1])
            # print("num_pred =", num_pred)
            sched_num = 0
            # print("self.pred[candidate_job - 1][1] =", self.pred[candidate_job - 1][1])
            for candidate_job_pred in self.pred[candidate_job - 1][1]:
                for i in range(len(self.scheduler)):
                    if candidate_job_pred == self.scheduler[i][0]:
                        sched_num += 1
            # print("sched_num =", sched_num)
            if sched_num == num_pred:
                succ = self.rank_oct.pop(0)[0]
                self.ready_list.append(succ)

    def sched_unentry_task(self, job):
        """scheduling unentry task"""
        label_pi = 0
        label_est = 0
        label_eft = 0
        min_o_eft = self.M
        for pi in range(1, self.q + 1):  # Scheduling on different processors.
            est = 0
            max_nm = 0
            for i in range(len(self.pred)):
                if job == self.pred[i][0]:  # Find the index position of predecessor i
                    job_pred = self.pred[i][1]
                    max_nm = self.pred_max_nm(pi, job_pred, job)

            # Computing the earliest time that processor can handle of task job.
            avail_pi = 0
            if pi in self.Pi.keys():
                avail_pi = self.Pi[pi][-1]['end']

            """get est"""
            if est < max(avail_pi, max_nm):
                est = max(avail_pi, max_nm)
            """get eft"""
            eft = est + self.computation_costs[job - 1][pi - 1]
            """get o_eft"""
            o_eft = eft + self.oct_table[job][pi - 1]
            """get min O_EFT(ni, pj)"""
            if min_o_eft > o_eft:
                min_o_eft = o_eft
                label_pi = pi
                label_est = est
                label_eft = eft
        # Join the pi list
        self.add_pi(label_pi, job, label_est, label_eft)

        """update ready_list"""
        self.update_ready_list()

    def peft(self):
        """algorithm entry"""
        self.start_time = time.time()
        """compute OCT table and rank_oct"""
        self.get_oct_table_and_rank_oct()

        """initial task"""
        n_entry = self.rank_oct.pop(0)[0]
        self.ready_list.append(n_entry)

        while self.ready_list:
            # print("ready_list =", self.ready_list)
            # print("rank_oct =", self.rank_oct)
            job = self.ready_list.pop(0)
            """entry task"""
            if job == n_entry:
                self.sched_entry_task(job)

            else:
                """unentry task"""
                self.sched_unentry_task(job)

        self.end_time = time.time()
        self.running_time = int(round((self.end_time - self.start_time), 3) * 1000)
        return self.makespan


if __name__ == "__main__":
    v = 20
    q = 7
    n = 55
    peft = Peft(v, q, n)
    makespan = peft.peft()
    print("-----------------------PEFT-----------------------")
    print('makespan =', makespan)
    print("Tlevel(PEFT) =", peft.Tlevel)
    print("Running_time =", peft.running_time)
    # print(peft.scheduler)
    # print(peft.Pi)
    print("-----------------------PEFT-----------------------")
    # print(peft.oct_table)
    # print(peft.Pi)
    # print(peft.rank_oct_copy)
    # print(peft.scheduler)
    """
    for n in range(1, N + 1):
        peft = PEFT(v, q, n)
        makespan = peft.peft()
        # print(peft.oct_table)
        # print(peft.Pi)
        # print(peft.rank_oct_copy)
        # print(peft.scheduler)
        if makespan == 0:
            print("----------------------")
            print(n)
            print("----------------------")
        else:
            print("makespan=", n, makespan)
    """

