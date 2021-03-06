# coding=utf-8
# import heft
import heft_new
import random
import copy
# import operator


class SchedEnv:     # no()
    """dag schedule environment"""
    def __init__(self, v, Q, t):
        """"""
        self.heft = heft_new.Heft(Q, t, v)
        self.pred = self.heft.pred_list()
        self.computation_costs = self.heft.computation_costs
        self.dag = self.heft.dag
        self.rank_u = self.heft.rank_u_copy
        # self.heft.heft()
        self.v = v                        # v is the number of nodes

        self.rank_u_copy = copy.deepcopy(self.rank_u)
        # self.pred = heft.pred_list()

        # self.q = len(self.computation_costs[0])  # the number of processors
        self.q = Q
        self.state = []
        self.state.append(self.v)
        for index in range(self.q):
            self.state.append(0)
        for index in range(self.q):
            self.state.append(self.computation_costs[0][index])

        self.next_state_ = []             # the number of remaining tasks n, est, wij
        self.scheduler = []              # tasks were scheduling on processors.[{1: 3}, {4: 1}, {3: 2}, ...]
        self.Pi = {}                     # the task information on processors

        self.reward_ = []
        self.makespan = 0

    def get_aft(self, job_pred_j):
        """"""
        aft = 0
        pred_pi = 0
        for k in range(len(self.rank_u_copy)):  # rank_u_copy
            if job_pred_j == self.rank_u_copy[k][0]:
                pred_pi = self.scheduler[k][job_pred_j]
                aft = 0
                for m in range(len(self.Pi[pred_pi])):
                    if self.Pi[pred_pi][m]['job'] == job_pred_j:
                        aft = self.Pi[pred_pi][m]['end']
        return aft, pred_pi

    def pred_max_nm(self, pi, job_pred_, job):
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
            if pi == pred_pi:
                cmi = 0
            else:
                cmi = self.dag[job_pred_[j]][job]

            if max_nm_ < aft + cmi:
                max_nm_ = aft + cmi
        return max_nm_

    def get_max_nm(self, job, p_i):
        """get the max_nm"""
        max_nm = 0
        for i in range(len(self.pred)):
            if job == self.pred[i][0]:  # Find the index position of predecessor i
                job_pred = self.pred[i][1]
                max_nm = self.pred_max_nm(p_i, job_pred, job)
        return max_nm

    def get_est(self, job, pi):
        """"""
        est_label = 0
        for p_i in range(1, self.q + 1):  # Scheduling on different processors.
            est = 0
            # job_pred = []
            """get the max_nm"""
            max_nm = self.get_max_nm(job, p_i)

            # Computing the earliest time that processor can handle of task job.
            avail_pi = 0
            if p_i in self.Pi.keys():
                avail_pi = self.Pi[p_i][-1]['end']

            if est < max(avail_pi, max_nm):
                est = max(avail_pi, max_nm)

            if len(self.next_state_) < 1 + self.q:
                self.next_state_.append(est)

            if p_i == pi:
                est_label = est
        return est_label

    def sched_other_jobs(self, job, pi, list_pi):
        """First computing max(n_m∈pred(n_i)){AFT(n_m ) + c_(m,i)}"""

        est_label = self.get_est(job, pi)

        # Join the pi list
        self.scheduler.append({job: pi})
        end = int(self.computation_costs[job - 1][pi - 1]) + int(est_label)
        if pi in self.Pi.keys():
            list_pi = list(self.Pi[pi])
            list_pi.append({'job': job, 'est': est_label, 'end': end})
            self.Pi[pi] = list_pi
        else:
            list_pi.append({'job': job, 'est': est_label, 'end': end})
            self.Pi[pi] = list_pi
        return est_label, end

    def step(self, action_):
        """get next_state, reward, done when input action"""
        reward_ = 0
        end = 0
        if self.rank_u:
            """have tasks unschedule"""
            first_job = self.rank_u.pop(0)
            job = first_job[0]
            pi = action_
            list_pi = []
            est = 0
            label_makespan = 0
            if job == 1:
                """scheduling the first job"""
                end = self.computation_costs[0][pi - 1]
                list_pi.append({'job': job, 'est': est, 'end': end})
                self.Pi[pi] = list_pi
                self.scheduler.append({job: pi})
                # self.reward_.append(- (end - est))

                """get next_state"""
                self.next_state_.append(self.v - 1)
                next_job = self.rank_u[0][0]
                self.get_est(next_job, pi)
                for index in range(self.q):
                    self.next_state_.append(self.computation_costs[next_job - 1][index])

            else:
                """scheduling the others jobs """
                self.state = self.next_state_
                for a in range(self.q):
                    if a+1 in self.Pi.keys() and label_makespan < self.Pi[a + 1][-1]['end']:
                        label_makespan = self.Pi[a + 1][-1]['end']
                    # print(self.Pi[a + 1][-1]['end'])

                # print(self.Pi)
                est, end = self.sched_other_jobs(job, pi, list_pi)
                # self.reward_.append(- (end - est))

                """get next_state"""
                self.next_state_ = []
                self.next_state_.append(len(self.rank_u))
                if len(self.rank_u) > 0:
                    next_job = self.rank_u[0][0]
                    self.get_est(next_job, pi)
                    for index in range(self.q):
                        self.next_state_.append(self.computation_costs[next_job - 1][index])

            # print("state =", self.state, "pi =", pi)
            if self.rank_u:
                if end < label_makespan:
                    self.reward_.append(0)
                    # print("max_makespan =", label_makespan)
                else:
                    # print("max_makespan =", label_makespan)
                    d = self.state[pi] + self.state[pi + self.q] - label_makespan
                    self.reward_.append(- d)
            else:
                # print("max_makespan =", label_makespan)
                d = self.state[pi] + self.state[pi + self.q] - label_makespan
                self.reward_.append(- d)
            reward_ = self.reward_[-1]
        """
        print("self.scheduler =", self.scheduler)
        print("self.Pi =", sorted(self.Pi.items(), key=operator.itemgetter(0)))
        """
        if self.rank_u:
            done_ = False
        else:
            done_ = True
            self.makespan = end

        return self.next_state_, reward_, done_

    def reset(self, v, Q, t):
        """"""
        # self.dag = heft.dag
        # self.computation_costs = heft.computation_costs
        self.heft = heft_new.Heft(Q, t, v)
        self.dag = self.heft.read_dag()
        self.computation_costs = self.heft.read_computation_costs()
        self.pred = self.heft.pred_list()
        # self.heft.heft()

        self.v = v  # v is the number of nodes
        self.rank_u = copy.deepcopy(self.rank_u_copy)
        self.rank_u_copy = copy.deepcopy(self.rank_u)
        # self.pred = heft.pred_list()

        self.q = len(self.computation_costs[0])  # the number of processors
        self.state = []
        self.state.append(self.v)
        for index in range(self.q):
            self.state.append(0)
        for index in range(self.q):
            self.state.append(self.computation_costs[0][index])
        self.next_state_ = []               # the number of remaining tasks n, est, wij
        self.scheduler = []                 # tasks were scheduling on processors.[{1: 3}, {4: 1}, {3: 2}, ...]
        self.Pi = {}                        # the task information on processors

        self.reward_ = []
        self.makespan = 0
        return self.state


if __name__ == "__main__":
    Q = 3
    n = 1
    V = 10

    env = SchedEnv(V, Q, n)
    print(env.state)

    print(env.dag)
    print(env.computation_costs)
    print(env.pred)
    print(env.rank_u)


    # num_pi = len(heft.computation_costs[0])
    num_pi = Q
    done = False
    e = 0
    makespans = []
    while e < 1:
        env.reset(V, Q, n)
        for n in range(V):
            action = random.randrange(1, Q + 1)  # random action is select Pj: 1-n
            next_state, reward, done = env.step(action)
            print("next_state =", next_state, "reward =", reward, "done =", done)
            print("--------------------------------------------------------------------------")

        print("env.scheduler =", env.scheduler)
        print("env.reward_ =", env.reward_)
        print("makespan =", env.makespan)
        print(sum(env.reward_))
        makespans.append(env.makespan)
        e += 1
        # print(min(makespans))


