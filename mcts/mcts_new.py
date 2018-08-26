
class State(object):
    """"""

    def __init__(self, v_, q_, n_):
        self.v = v_
        self.q = q_
        self.n = n_
        self.dag = {}
        self.computation_costs = []
        self.Pi = {}
        self.tasks_proces_mapping = []
        self.ready_queue = [1, ]

        self.current_value = 0.0
        self.sched_actions = []
        self.ACTIONS = [a for a in range(1, q_ + 1)]

    def read_dag(self):
        """q is the number of processors, n is which graph"""
        filename = 'E:/PycharmProjects/dag/save_dag/new/v=' + str(self.v) + 'q=' + str(self.q) + '/_' + str(self.n) + '_dag_q=' \
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

    def schedule(self):
        """"""
        self.read_dag()
        self.read_computation_costs()

        job = self.ready_queue.pop(0)
        print("job= ", job)
        print(self.ready_queue)
        while job < 10:
            action = random.choice(self.ACTIONS)
            print("action =", action)
            # job = self.ready_queue.pop(0)
            job += 1



    def get_current_value(self):
        return self.current_value

    def set_current_value(self, value):
        self.current_value = value

    def get_sched_actions(self):
        return self.sched_actions

    def set_sched_actions(self, actions):
        self.sched_actions = actions

    def is_terminal(self, node_):
        if node_ == self.v:
            return True
        else:
            return False

    def compute_reward(self):
        return -abs(1 - self.current_value)

    def get_next_state(self, q_):
        random_action = random.choice([action for action in self.ACTIONS])

        next_state = State(q_)
        makespan = 0
        reward = - makespan
        next_state.set_current_value(self.current_value + reward)
        next_state.set_sched_actions(self.sched_actions + [random_action])
        return next_state

    def __repr__(self):
        return "State: [state: {}, value: {}, actions: {}]".format(self.ready_queue, self.current_value, self.sched_actions)


class Node(object):
    """"""

    def __init__(self, q_):
        self.q = q_
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0

        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def set_visit_times(self, times):
        self.visit_times = times

    def get_quality_value(self):
        return self.quality_value

    def set_quality_value(self, value):
        self.quality_value = value

    def quality_value_add_n(self, n):
        self.quality_value += n

    def is_all_expand(self):
        if len(self.children) == self.q:
            return True
        else:
            return False

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    def __repr__(self):
        return "Node: [Q/N: {}/{}, state: {}]".format(
            self.quality_value, self.visit_times, self.state)