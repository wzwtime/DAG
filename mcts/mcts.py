# coding=utf-8
"""Monte Carlo Tree Search Methods(MCTS) 2018-08-10"""
import math
import time
import random
from algorithms import heft_new
import copy


class UCTSearch:

    def __init__(self, v_, q_, n_,  max_round_num, max_time):
        """parameters"""
        self.v = v_
        self.q = q_
        self.n = n_
        self.MAX_ROUND_NUMBER = max_round_num
        self.MAX_TIME = max_time
        """get rank_u from HEFT """
        self.heft = heft_new.Heft(q_, n_, v_, 0)
        self.heft_makespan = self.heft.heft()
        # self.pred = self.heft.pred_list()
        self.pred = self.heft.pred
        self.computation_costs = self.heft.computation_costs
        self.dag = self.heft.dag
        self.rank_u = self.heft.rank_u_copy
        self.rank_u_copy = copy.deepcopy(self.rank_u)

        self.Pi = {}
        self.scheduler = []
        """others"""
        self.ready_queue = []
        for job in self.rank_u:
            self.ready_queue.append(job[0])
        self.ready_queue_copy = copy.deepcopy(self.ready_queue)
        self.start_time = 0
        self.end_time = 0
        self.running_time = 0
        self.tree = {}
        """
        tree = {
                0: N
                job: [
                        [[p1], [N, q]], 
                        [[p2], [N, q]], 
                        ..., 
                        [[Pq], [N, q]],
                    ]
                ...
                }
        tree = {
                0: N
                1 :[
                    [[1], [N, q]], 
                    [[2], [N, q]],
                     ..., 
                    [[q], [N, q]]
                ]
                4 :[
                    [[1, 1],[N, q]], 
                    [[1, 2],[N, q]], 
                    ..., 
                    [[q, q],[N, q]]
                ]
                 ...
                10 :[
                    [[1, 1, ..., 1],[N, q]], 
                    ...,
                    [[2, 2, ..., 2],[N, q]], 
                    ..., 
                    [[q, q, ..., q],[N, q]]
                ]
                }
        """

        self.path = []
        """
        path = [[job1, p1], [job4, p2], ..., [job8, p3]]
        """
        self.actions = [a for a in range(1, q_ + 1)]
        # self.select_actions = []
        self.best_makespan = 0
        self.pi_list = []
        self.N_v = 0        # the number of patent visit
    """
    def read_dag(self):
        # q is the number of processors, n is which graph
        filename = 'E:/PycharmProjects/dag/save_dag/new/v=' + str(self.v) + 'q=' + str(self.q) + '/_' + str(self.n) \
                   + '_dag_q=' + str(self.q) + '.txt'
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
        # q is the number of processors, n is which graph
        filename = 'E:/PycharmProjects/dag/save_dag/new/v=' + str(self.v) + 'q=' + str(self.q) + '/_' + str(self.n) \
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
    """
    def mcts_uct(self, cp_):
        # Run as much as possible under the computation budget
        start_time = time.time()
        running_time = 0

        nn = 1
        while running_time < self.MAX_TIME:
            print("----------------------------------", nn)
            print("self.tree =", self.tree)
            self.ready_queue = copy.deepcopy(self.ready_queue_copy)     # deepcopy()
            # 1. Find the best node to expand
            # job_pi_list, pi_ = self.tree_policy()
            self.tree_policy(cp_)

            # 2. Random run to add node and get reward
            # makespan = self.default_policy(job_, pi_)
            makespan = self.default_policy()

            # 3. Update all passing nodes with reward
            self.backup(makespan)

            end_time = time.time()
            running_time = end_time - start_time
            nn += 1
            # print("self.tree =", self.tree)
        # N. Get the best next node
        # best_makespan = self.best_child()

    def tree_policy(self, cp_):
        """"""
        # job_ = self.ready_queue.pop(0)
        job_ = self.ready_queue[0]
        # clear pi_list
        self.pi_list = []

        best_pi = 0
        k = 0
        # Check if the current node is the terminal node
        while job_ != self.v:

            if job_ not in self.tree.keys():
                self.tree[job_] = []
                return self.expand(job_, best_pi)
            else:
                # judge node is all expand
                print(job_, "in the tree.")

                print("-----path =", self.path)
                # print("--------------self.pi_list=", self.pi_list)
                count = 0
                if self.path:
                    for item in self.tree[job_]:
                        # if item[0][0] == self.path[-1][1]:
                        if item[0][: len(self.pi_list)] == self.pi_list:
                            count += 1
                else:
                    count = len(self.tree[job_])
                if count != self.q:
                    print("No all expand")
                    return self.expand(job_, best_pi)
                else:
                    print("Yes all expand")
                    # cp = round(1.0 / math.sqrt(2), 2)
                    cp = cp_
                    best_pi = self.best_child(job_, cp)

                    # record path pi
                    self.pi_list.append(best_pi)

                    # record the parent path
                    self.path.append([job_, best_pi])

                """
                if len(self.tree[job_] ) != self.q:
                    print("No all expand")
                    return self.expand(job_, best_pi)
                else:
                    print("Yes all expand")
                    cp = round(1.0 / math.sqrt(2), 2)
                    best_pi = self.best_child(job_, cp)
                    # record the parent path
                    self.path.append([job_, best_pi])
                """

            # job_ = self.ready_queue.pop(0)
            k += 1
            job_ = self.ready_queue[k]
            # job_list.append(job_)

        # Return the leaf node
        return job_

    def expand(self, job_, best_pi_):
        """"""
        self.actions = [a for a in range(1, self.q + 1)]
        info = []
        # pi_list = []

        # get available action
        if self.tree[job_]:
            # print("---pi_list =", self.pi_list)
            for i in range(len(self.tree[job_])):
                # self.actions.remove(self.tree[job_][i][0][-1])  # [-1]
                if self.tree[job_][i][0][:len(self.pi_list)] == self.pi_list:
                    self.actions.remove(self.tree[job_][i][0][-1])      # [-1]

        # random action
        pi = random.choice(self.actions)

        # select best parent action
        if best_pi_ == 0:
            info = [[pi], [0, 0]]
            self.pi_list.append(pi)
        else:
            # pi_list.append(best_pi_)
            # pi_list.append(pi)
            # info.append(pi_list)

            self.pi_list.append(pi)
            info.append(self.pi_list)
            info.append([0, 0])

        # add info into the tree
        self.tree[job_].append(info)

        # record the child path
        self.path.append([job_, pi])
        # print("path =", self.path)

        print("expand tree =", self.tree)
        return self.path

    def best_child(self, job_, cp_):
        """# UCB = quality / times + C * sqrt(2 * ln(total_times) / times)"""
        # Travel all sub nodes to find the best one
        best_score = float('-Inf')
        best_pi = 0
        best_pi_index = 0
        """all expand get ucb"""
        for i in range(len(self.tree[job_])):
            # only compare the state that best_pi = pi_list. [1, 2],[1, 3], [2, 3](no compare), [1, 1]
            if self.tree[job_][i][0][:len(self.pi_list)] == self.pi_list:
                # print("------------------------self.pi_list =", self.pi_list)

                left = round(self.tree[job_][i][1][1]*1.0/self.tree[job_][i][1][0], 2)
                if job_ == 1:
                    right = round(2.0 * math.log(self.tree[0]) / self.tree[job_][i][1][0], 2)
                else:
                    right = round(2.0 * math.log(self.N_v) / self.tree[job_][i][1][0], 2)

                # right = round(2.0 * math.log(self.tree[0] / self.tree[job_][i][1][0]), 2)
                """
                if len(self.pi_list) == 1:
                    right = round(2.0 * math.log(self.tree[0] / self.tree[job_][i][1][0]), 2)
                else:
                    right = round(2.0 * math.log(self.tree[job_][i][1][0] / self.tree[job_][i][1][0]), 2)
                """
                score = round(left + cp_ * math.sqrt(right), 2)
                print(left, right, score)
                if score > best_score:
                    best_score = score
                    best_pi = self.tree[job_][i][0][-1]  # [-1]
                    best_pi_index = i

            """
            left = self.tree[job_][i][1][1]
            right = round(2.0 * math.log(self.tree[0] / self.tree[job_][i][1][0]), 2)
            score = round(left + cp_ * math.sqrt(right), 2)
            print(left, right, score)
            if score > best_score:
                best_score = score
                best_pi = self.tree[job_][i][0][-1]     # [-1]
                # best_pi = self.tree[job_][i][0][0]
            """
        print("best_score =", best_score)
        print("best_pi =", best_pi)
        self.N_v = self.tree[job_][best_pi_index][1][0]
        return best_pi

    def add_pi(self, pi_, job_, est_, eft_):
        """Join the task to the list and add the task to the schedule list"""
        list_pi = []
        if pi_ in self.Pi.keys():
            list_pi = list(self.Pi[pi_])
            list_pi.append({'job': job_, 'est': est_, 'end': eft_})
            self.Pi[pi_] = list_pi
            self.scheduler.append([job_, pi_])
            # self.select_actions.append(pi_)
        else:
            list_pi.append({'job': job_, 'est': est_, 'end': eft_})
            self.Pi[pi_] = list_pi
            self.scheduler.append([job_, pi_])
            # self.select_actions.append(pi_)

    def get_aft(self, job_pred_j):
        """"""
        aft = 0
        pred_pi = 0
        for k in range(len(self.rank_u_copy)):  # rank_u_copy
            if job_pred_j == self.rank_u_copy[k][0]:
                # pred_pi = self.scheduler[k][job_pred_j]   # scheduler = {}
                pred_pi = self.scheduler[k][1]              # scheduler = []
                aft = 0
                for m in range(len(self.Pi[pred_pi])):
                    if self.Pi[pred_pi][m]['job'] == job_pred_j:
                        aft = self.Pi[pred_pi][m]['end']
        return aft, pred_pi

    def pred_max_nm(self, p_i, job_pred_, job_):
        """The maximum time spent on a precursor node."""
        max_nm_ = 0
        for j in range(len(job_pred_)):
            # print(job_pred_[j])
            # Finding the completion time of the predecessor.1）Finding which processor the predecessor is on
            #  2）Finding the processor index location 3）Output the value of 'end'

            job_pred_j = job_pred_[j]
            """get aft"""

            aft, pred_pi = self.get_aft(job_pred_j)

            # computing cmi
            if p_i == pred_pi:
                cmi = 0
            else:
                cmi = self.dag[job_pred_[j]][job_]

            if max_nm_ < aft + cmi:
                max_nm_ = aft + cmi
        return max_nm_

    def get_max_nm(self, job_, p_i):
        """get the max_nm"""
        max_nm = 0
        for i in range(len(self.pred)):
            if job_ == self.pred[i][0]:  # Find the index position of predecessor i
                job_pred = self.pred[i][1]
                max_nm = self.pred_max_nm(p_i, job_pred, job_)
        return max_nm

    def get_est(self, job_, pi_):
        """"""
        est_label = 0
        for p_i in range(1, self.q + 1):  # Scheduling on different processors.
            est = 0
            # job_pred = []
            """get the max_nm"""
            max_nm = self.get_max_nm(job_, p_i)

            # Computing the earliest time that processor can handle of task job.
            avail_pi = 0
            if p_i in self.Pi.keys():
                avail_pi = self.Pi[p_i][-1]['end']

            if est < max(avail_pi, max_nm):
                est = max(avail_pi, max_nm)
            if p_i == pi_:
                est_label = est
        return est_label

    # def default_policy(self, job_, pi_):
    def default_policy(self):
        """"""
        self.Pi = {}
        self.scheduler = []
        self.actions = [a for a in range(1, self.q + 1)]
        selected_action = copy.deepcopy(self.pi_list[1:])   # delete 1

        est = 0
        eft = 0
        next_pi = 0

        print("-----default_policy path =", self.path)

        job_ = self.ready_queue.pop(0)
        pi_ = self.path[0][1]
        if job_ == 1:
            eft = self.computation_costs[job_-1][pi_-1]
            self.add_pi(pi_, job_, est, eft)

        while self.ready_queue:
            # print("++++++++")
            next_job = self.ready_queue.pop(0)
            # get select action
            if selected_action:
                next_pi = selected_action.pop(0)
            else:
                next_pi = random.choice(self.actions)
            """
            for i in range(1, len(self.path)):
                job_, pi_ = self.path[i][0], self.path[i][1]
                print("---------", next_job, job_, pi_)
                if next_job == job_:
                    next_pi = pi_
                    break
                else:
                    next_pi = random.choice(self.actions)
                    break
            """
            est = self.get_est(next_job, next_pi)
            eft = int(self.computation_costs[next_job - 1][next_pi - 1]) + int(est)
            self.add_pi(next_pi, next_job, est, eft)
        print("makespan =", -eft)
        # print("self.Pi =", self.Pi)
        return -eft

    def backup(self, makespan):
        """Update util the root node"""
        # count + 1
        self.tree[0] += 1

        print("self.path =", self.path)
        print("---pi_list=", self.pi_list)
        # Update the quality value

        # update num
        for i in range(len(self.pi_list)):
            path = self.path.pop(0)
            job = path[0]
            pi = path[1]
            for j in range(len(self.tree[job])):
                # if self.tree[job][j][0][: i + 1] == self.pi_list[: i + 1]:
                if self.tree[job][j][0] == self.pi_list[:i+1]:
                    self.tree[job][j][1][0] += 1
                    q_v = self.tree[job][j][1][1]

                    # update child q = q_v + makespan + est
                    for ii in range(len(self.Pi[pi])):
                        if self.Pi[pi][ii]['job'] == job:
                            est = self.Pi[pi][ii]['est']
                    # print("Pi =", self.Pi)
                    print("-----est", est)
                    new_q = q_v + makespan + est
                    self.tree[job][j][1][1] = new_q
                    print("update tree--", self.tree)
                    """
                    if est == 0:
                        new_q = q_v + makespan
                        parent_q = new_q
                        # update
                        self.tree[job][j][1][1] = new_q
                        print("update tree---1", self.tree)
                    # elif self.tree[job][j][0] == self.pi_list:
                    else:
                        # new_q = parent_q + est
                        # parent_q = new_q
                        new_q = q_v + makespan + est
                        # makespan = makespan + est
                        # update
                        self.tree[job][j][1][1] = new_q
                        print("update tree---2", self.tree)
                    """

        """
        while self.path:
            path = self.path.pop(0)
            job = path[0]
            pi = path[1]
            for i in range(len(self.tree[job])):
                # satisfy many pi
                if self.tree[job][i][0][-1] == pi:
                # if self.tree[job][i][0] == self.pi_list:
                    # n_v + 1
                    self.tree[job][i][1][0] += 1
                    n_v = self.tree[job][i][1][0]
                    q_v = self.tree[job][i][1][1]

                    # update child q = parent_q - est
                    for ii in range(len(self.Pi[pi])):
                        if self.Pi[pi][ii]['job'] == job:
                            est = self.Pi[pi][ii]['est']
                    # print("Pi =", self.Pi)
                    print("-----est", est)

                    if est == 0:
                        # first
                        if n_v == 1:
                            new_q = round((q_v + makespan) * 1.0 / n_v, 2)
                            parent_q = new_q
                        # get average
                        else:
                            new_q = round((q_v + makespan) * 1.0 / 2, 2)
                            parent_q = new_q
                        # update
                        self.tree[job][i][1][1] = new_q
                        print("update tree---1", self.tree)
                    # else:
                    #     new_q = parent_q + est
                    #     parent_q = new_q
                    elif self.tree[job][i][0] == self.pi_list:
                        new_q = parent_q + est
                        parent_q = new_q
                        # update
                        self.tree[job][i][1][1] = new_q
                        print("update tree---2", self.tree)
                    # self.tree[job][i][1][1] = new_q
        """
    def main(self, cp_):
        """return makespan"""
        self.start_time = time.time()
        self.tree[0] = 0

        round_num = 0
        self.MAX_ROUND_NUMBER = 1

        while round_num < self.MAX_ROUND_NUMBER:
            self.mcts_uct(cp_)
            round_num += 1

        self.end_time = time.time()
        self.running_time = self.end_time - self.start_time

        return max(self.tree[1], key=lambda item: item[1][1]/item[1][0])[1][1]/\
               max(self.tree[1], key=lambda item: item[1][1]/item[1][0])[1][0]


if __name__ == "__main__":
    v = 10
    q = 3
    n = 1
    MAX_ROUND_NUMBER = 1
    MAX_TIME = 600  # s
    cp = 10
    # cp = round(1.0 / math.sqrt(2), 2)

    mcts = UCTSearch(v, q, n, MAX_ROUND_NUMBER, MAX_TIME)
    print("best_makespan =", mcts.main(cp))
    print("heft_makespan =", mcts.heft_makespan)
    # print("ready_queue =", mcts.ready_queue)
