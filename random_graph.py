# coding=utf-8
"""random_graph_generator2018-06-05"""
import operator
import random
import math
import os
import time


class RandomGraphGenerator:

    def __init__(self, v_, q_,  N_, n_min_, n_max_):
        self.SET_v = [20, 40, 60, 80, 100]
        self.SET_ccr = [0.1, 0.5, 1.0, 5.0, 10.0]
        # self.SET_ccr = [1.0, 5.0, 10.0]
        # self.SET_alpha = [0.5, 1.0, 2.0]
        self.SET_alpha = [1.0, 2.0]
        self.SET_out_degree = [2, 3, 4, 5, ]
        self.SET_beta = [0.1, 0.25, 0.5, 0.75, 1.0]
        """add new info"""
        # self.SET_density = [0.2, 0.5, 0.8]  # 稀疏程度
        self.SET_density = [0.2, 0.5, 0.8, 1.0]  # 稀疏程度
        self.SET_jump = [1, 2, 4, ]

        self.computation_costs = []
        self.dag = {}
        self.avg_w_dag = 0
        self.height = 0
        self.width = 0
        self.v = v_
        self.q = q_
        self.N = N_
        self.n_min = n_min_
        self.n_max = n_max_
        self.mon = time.localtime(time.time())[1]
        self.day = time.localtime(time.time())[2]

    def random_avg_w_dag(self, n_min_, n_max_):
        """Randomly generated average computation costs"""
        self.avg_w_dag = random.randint(n_min_, n_max_)
        return self.avg_w_dag

    def get_wij(self, n_, beta):
        """Generate computation costs overhead for tasks on different processors"""
        self.random_avg_w_dag(self.n_min, self.n_max)

        file_path_ = 'save_dag/' + str(self.mon) + "_" + str(self.day) + '/v=' + str(self.v) + 'q=' + str(self.q) + '/'
        # filename = file_path_ + '_' + str(n_) + '_computation_costs_q=' + str(self.q) + '.txt'
        filename = file_path_ + '_' + str(n_) + '_comp_costs' + '.txt'
        file_dir_ = os.path.split(filename)[0]
        if not os.path.isdir(file_dir_):
            os.makedirs(file_dir_)
        if os.path.exists(filename):
            os.remove(filename)  # remove

        for i in range(self.v):
            avg_w = random.randint(1, 2 * self.avg_w_dag)
            for j in range(self.q):
                wij = random.randint(math.ceil(avg_w * (1 - beta / 2)), math.ceil(avg_w * (1 + beta / 2)))
                with open(filename, 'a') as file_object2:
                    if j < self.q - 1:
                        info1 = str(wij) + "  "
                        file_object2.write(info1)
                    else:
                        info1 = str(wij) + "\n"
                        file_object2.write(info1)

    def get_height_width(self, alpha):
        """get_height_width"""
        mean_height = math.ceil(math.sqrt(self.v) / alpha)       # Round up and calculate the average
        mean_width = math.ceil(alpha * math.sqrt(self.v))        # Round up and calculate the average
        self.height = random.randint(1, 2 * mean_height - 1)   # uniform distribution
        self.width = random.randint(2, 2 * mean_width - 2)     # uniform distribution

    def number_nodes_layer(self, sum_m, num_second_layer):
        """determine the number of nodes in each layer of the graph"""
        task_num_layer = []
        for t in range(self.height - 4):
            task_num_layer.append(2)
        for k in range(sum_m - 2 * (self.height - 4)):
            rand_index = random.randint(0, self.height - 5)
            if task_num_layer[rand_index] < self.width:
                task_num_layer[rand_index] += 1
            else:
                min_n = min(task_num_layer)
                min_index = task_num_layer.index(min_n)
                task_num_layer[min_index] += 1
        task_num_layer.insert(0, 1)                     # the first layer
        task_num_layer.insert(1, num_second_layer)      # the second layer
        task_num_layer.insert(int(self.height / 2), self.width)   # width
        task_num_layer.append(1)                        # the last layer
        return task_num_layer

    def order_dag(self, task_num_layer, out_degree):
        """Order the number of nodes per layer according to the out-degree"""
        for j in range(self.height - 1):
            for i in range(self.height - 1):
                if task_num_layer[i] * out_degree < task_num_layer[i + 1]:
                    temp = task_num_layer[i]
                    task_num_layer[i] = task_num_layer[i + 1]
                    task_num_layer[i + 1] = temp
                    # task_num_layer[i], task_num_layer[i + 1] = task_num_layer[i + 1], task_num_layer[i]
                    #  don't use temp
        return task_num_layer

    def get_dag_id(self, task_num_layer):
        """Convert the number of nodes per layer to sequential task numbers."""
        dag_id = []
        num = 0
        for i in range(self.height):
            dag_id_temp = []
            for j in range(int(task_num_layer[i])):
                num += 1
                dag_id_temp.append(num)
            dag_id.append(dag_id_temp)
        return dag_id

    def the_first_layer(self, dag_id, avg_comm_costs):
        """the first layer"""
        temp_dag = {}
        for i in range(len(dag_id[1])):  # the first layer
            index = dag_id[1][i]
            communication_costs = random.randint(1, 2 * avg_comm_costs - 1)
            temp_dag[index] = communication_costs
        self.dag[1] = temp_dag

    def second_to_last_layer(self, dag_id, avg_comm_costs):
        """Second-to-last layer"""
        for i in range(len(dag_id[self.height - 2])):
            temp_dag = {}                        # Attention!!!!!!!!!!! Prevents generator the same communication costs
            index = dag_id[self.height - 2][i]
            dag_index = dag_id[self.height - 1][0]
            communication_costs = random.randint(1, 2 * avg_comm_costs - 1)
            temp_dag[dag_index] = communication_costs
            self.dag[index] = temp_dag

    def grouping_children_nodes(self, p_num, c_num, out_degree):
        """Grouping children's nodes"""
        temp_child_num = []
        for j in range(p_num):
            temp_child_num.append(1)
        for k in range(c_num - p_num):
            rand_index = random.randint(0, p_num - 1)
            if temp_child_num[rand_index] < out_degree:
                temp_child_num[rand_index] += 1
            else:
                min_n = min(temp_child_num)
                min_index = temp_child_num.index(min_n)
                temp_child_num[min_index] += 1
        return temp_child_num

    def add_edges(self, p_id_list, p_num, out_degree, c_id_list, c_num, avg_comm_costs):
        # print("p_id_list=", p_id_list, "c_id_list=", c_id_list)
        random.shuffle(p_id_list)  # Disrupt the p_id_list
        # print("p_id_list =", p_id_list)
        temp_pid = p_id_list[0]     # 选择打乱后的第一个pid增加边信息
        # print("temp_pid =", temp_pid)

        """Calculation out_degree of temp_pid"""
        # print("self.dag[temp_pid] =", self.dag[temp_pid])
        o_degree = len(self.dag[temp_pid])

        # print("o_degree =", o_degree)
        edge_num = math.ceil(p_num * self.SET_density[random.randrange(0, 2)])      # 根据稀疏程度计算该节点的出度
        # print("edge_num =", edge_num)

        if edge_num > out_degree:
            edge_num = out_degree

        if edge_num > o_degree:     # 判断是否可以为temp_pid增加边
            # print("yes")
            random.shuffle(c_id_list)  # Disrupt the c_id_list
            # print("c_id_list =", c_id_list)
            edge_num_count = 0
            temp_dag = {}
            for key_, value_ in self.dag[temp_pid].items():  # add old info
                # print("key, value =", key_, value_)
                temp_dag[key_] = value_
            for t in range(c_num):
                c_id = c_id_list[t]
                if c_id not in self.dag[temp_pid].keys():   # 添加未添加过的边
                    edge_num_count += 1
                    # print("c_id =", c_id)
                    communication_costs = random.randint(1, 2 * avg_comm_costs - 1)
                    temp_dag[c_id] = communication_costs

                if edge_num_count == edge_num - o_degree:
                    self.dag[temp_pid] = temp_dag
                    # print("self.dag[temp_pid] =", self.dag[temp_pid])
                    break

    def less_to_multi(self, task_num_layer, out_degree, dag_id, avg_comm_costs):
        """Less-to-multi make child nodes are randomly divided into total number of parent nodes"""
        # p_id_list = []
        # c_id_list = []
        for i in range(1, len(task_num_layer) - 2):
            p_num = task_num_layer[i]
            c_num = task_num_layer[i + 1]
            if p_num != 1 and c_num != 1 and p_num <= c_num:
                """clear empty!18.10.31 !!!!!!!!!!!!!!!!!!!"""
                p_id_list = []
                c_id_list = []
                p_index = i
                """Grouping children's nodes"""
                temp_child_num = self.grouping_children_nodes(p_num, c_num, out_degree)

                """Traversing every parent node of the index."""
                sum_num = 0
                sum_list = 0
                for j in range(p_num):
                    temp_dag = {}
                    p_id = dag_id[p_index][j]
                    p_id_list.append(p_id)
                    """Determination of child node number."""
                    """
                    sum_num = p_id + p_num - j - 1    # The last parent node number
                    print("last_parent_id = ", sum_num)
                    """
                    if j > 0:
                        sum_list += temp_child_num[j - 1]
                    """View subnode number"""
                    for k in range(temp_child_num[j]):
                        if j == 0:
                            sum_num = p_id + p_num - j - 1 + k + 1
                        elif j > 0:
                            sum_num = p_id + p_num - j - 1 + k + 1 + sum_list
                        """assign communication costs"""
                        communication_costs = random.randint(1, 2 * avg_comm_costs - 1)
                        c_id_list.append(sum_num)
                        temp_dag[sum_num] = communication_costs
                    # print(p_id, "-->", temp_dag)
                    self.dag[p_id] = temp_dag

                """add more edge"""
                self.add_edges(p_id_list, p_num, out_degree, c_id_list, c_num, avg_comm_costs)

    def grouping_parent_nodes(self, p_num, c_num):
        """Grouping children's nodes"""
        temp_parent_num = []
        for j in range(c_num):
            temp_parent_num.append(1)
        for k in range(p_num - c_num):
            rand_index = random.randint(0, c_num - 1)
            temp_parent_num[rand_index] += 1
        return temp_parent_num

    def multi_to_less(self, task_num_layer, dag_id, avg_comm_costs, out_degree):
        """Multi-to-Less make parent nodes are randomly divided into total number of child nodes"""
        # p_id_list = []
        # c_id_list = []

        for i in range(2, len(task_num_layer) - 1):     # !!!!!!!!!!!!!  is -1 not -2  Traverse completely
            p_num = task_num_layer[i - 1]
            c_num = task_num_layer[i]

            if p_num != 1 and c_num != 1 and p_num > c_num:
                """clear empty!18.10.31 !!!!!!!!!!!!!!!!!!!"""
                p_id_list = []
                c_id_list = []
                c_index = i
                """The parent node is randomly divided into the total number of child nodes."""
                temp_parent_num = self.grouping_parent_nodes(p_num, c_num)

                """Traversing every child node of the index."""
                # print("p_num =", p_num, "c_num =", c_num)

                length_parent = 0
                for j in range(c_num):
                    c_id = dag_id[c_index][j]
                    c_id_list.append(c_id)

                    first_parent_id = c_id - p_num
                    """View parent node id"""
                    for k in range(temp_parent_num[j]):
                        length_parent += 1
                        p_id = first_parent_id + length_parent - j - 1

                        p_id_list.append(p_id)
                        """assign communication costs"""
                        temp_dag = {}        # Attention!!!!!!!!!!! Prevents generator the same communication costs
                        communication_costs = random.randint(1, 2 * avg_comm_costs - 1)
                        temp_dag[c_id] = communication_costs
                        # print(p_id, "--->", c_id)
                        self.dag[p_id] = temp_dag
                """add edges"""
                # self.add_edges(p_id_list, p_num, out_degree, c_id_list, c_num, avg_comm_costs)

    def random_graph_generator(self, n_, ccr, alpha, out_degree, beta):
        """requires five parameters to build weighted DAGs
        v: number of tasks in the graph
        ccr: average communication cost to average computation cost
        alpha: shape parameter of the graph
        out_degree: out degree of a node
        beta: range percentage of computation costs on processors
        q: number of processors"""

        """Determine whether it can constitute a DAG"""
        mean_height = math.ceil(math.sqrt(self.v) / alpha)  # Round up and calculate the average
        mean_width = math.ceil(alpha * math.sqrt(self.v))   # Round up and calculate the average
        self.height = random.randint(1, 2 * mean_height - 1)
        self.width = random.randint(2, 2 * mean_width - 2)  # uniform distribution with a mean value equal to mean_width

        min_num = min(self.width, out_degree)

        while True:
            num_second_layer = random.randint(2, min_num)
            sum_m = self.v - 2 - num_second_layer - self.width

            if (self.height - 4) * self.width >= sum_m and (2 * (self.height - 4) <= sum_m):
                print("yes")
                break
            else:
                self.get_height_width(alpha)     # random generator a new h,w
                while (self.height - 2) * self.width < self.v - 2:
                    self.get_height_width(alpha)  # random generator a new h,w

        """ 1) The first is to determine the number of nodes in each layer of the graph"""
        task_num_layer = self.number_nodes_layer(sum_m, num_second_layer)

        """Order the number of nodes per layer according to the out-degree"""
        task_num_layer = self.order_dag(task_num_layer, out_degree)

        """Convert the number of nodes per layer to sequential task numbers."""
        dag_id = self.get_dag_id(task_num_layer)

        """If there is one node of the dag's first layer,it's a truly dag."""
        if task_num_layer[0] == 1:
            print("v =", self.v, "height = ", self.height, "width =", self.width, "CCR =", ccr, "Alpha =", alpha,
                  "out_degree =", out_degree, "beta =", beta, "Number of Processors =", self.q)
            print("ordered task_num_layer:", task_num_layer)
            print("dag_id = ", dag_id)

            """Generate computation costs on different processors for every task"""
            self.get_wij(n_, beta)

            """Average communication costs"""
            avg_comm_costs = math.ceil(ccr * self.avg_w_dag)  # Rounded up

            """2)Then according to the out-degree to determine the vertex connection relationship,
            allocation of communication costs"""
            """1.the first layer"""
            self.the_first_layer(dag_id, avg_comm_costs)

            """2.Second-to-last layer"""
            self.second_to_last_layer(dag_id, avg_comm_costs)

            """3.Other layers that remove the last layer"""

            """3.1 Less-to-multi make child nodes are randomly divided into total number of parent nodes"""
            self.less_to_multi(task_num_layer, out_degree, dag_id, avg_comm_costs)

            """3.2 Multi-to-Less make parent nodes are randomly divided into total number of child nodes"""
            self.multi_to_less(task_num_layer, dag_id, avg_comm_costs, out_degree)

            """4.The last layer"""
            self.dag[self.v] = {}
        else:
            print("DAG Error! Get a new DAG!")
            self.random_graph_generator(n_, ccr, alpha, 5, beta)      # Get a new DAG

    def random_index(self, set_):
        """Get the random index i of the collection to determine which parameter in the collection"""
        length = len(set_)
        index_ = random.randint(1, length) - 1
        return index_

    def write_graph_parameter(self, ccr, alpha, beta):
        """"""
        file_path_ = 'graph_parameter/' + str(self.mon) + "_" + str(self.day) + '/v=' + str(self.v) + 'q=' + str(self.q)
        filename = file_path_ + '.txt'
        file_dir_ = os.path.split(filename)[0]
        if not os.path.isdir(file_dir_):
            os.makedirs(file_dir_)
        # with open(filename, 'w') as file_object_:
        with open(filename, 'a') as file_object_:
            info_ = str(self.v) + "  " + str(ccr) + "  " + str(alpha) + "  " + str(beta) + "  " + str(self.q) + "\n"
            file_object_.write(info_)

    def select_parameter(self, n_):
        """Select 3 parameters"""
        ccr = self.SET_ccr[self.random_index(self.SET_ccr)]
        alpha = self.SET_alpha[self.random_index(self.SET_alpha)]
        beta = self.SET_beta[self.random_index(self.SET_beta)]

        """random_graph_generator"""
        self.random_graph_generator(n_, ccr, alpha, 5, beta)

        """Write graph parameter to file"""
        self.write_graph_parameter(ccr, alpha, beta)


if __name__ == "__main__":
    v = 100
    # q = 3
    N = 1
    n_min = 5
    n_max = 20
    for q in range(3, 8):
        rgg = RandomGraphGenerator(v, q, N, n_min, n_max)

        def store_dag(n_):
            file_path = 'save_dag/' + str(rgg.mon) + "_" + str(rgg.day) + '/v=' + str(v) + 'q=' + str(q) + '/'
            # filename_ = file_path + "_" + str(n_) + '_dag_q=' + str(q) + '.txt'
            filename_ = file_path + "_" + str(n_) + '_comm_costs' + '.txt'
            file_dir = os.path.split(filename_)[0]
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if os.path.exists(filename_):
                os.remove(filename_)

            for m in range(len(dag_new)):
                task_id = dag_new[m][0]
                # for key, value in dag1[m][1].items():
                for key, value in sorted(dag_new[m][1].items()):  # Ascending sort children task number
                    succ_id = key
                    succ_weight = value
                    with open(filename_, 'a') as file_object:
                        info = str(task_id) + "  " + str(succ_id) + "  " + str(succ_weight) + "\n"
                        file_object.write(info)

        n = 1
        while n <= N:
            """"execute"""
            rgg.select_parameter(n)

            """Ascending sort by task number"""
            dag_new = sorted(rgg.dag.items(), key=operator.itemgetter(0))

            """Store DAG in files"""
            store_dag(n)
            n += 1
