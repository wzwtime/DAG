

def read_dag(self):
    """q is the number of processors, n is which graph"""
    # dag_ = {}
    filename = 'save_dag' + '/' + 'new/v=' + str(self.v) + 'q=' + str(self.Q) + '/_' + str(self.n) + '_dag_q=' \
               + str(self.Q) + '.txt'
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
            # dag_[task_id] = succ_dict
            self.dag[task_id] = succ_dict
        # dag_[task_id + 1] = {}
        self.dag[task_id + 1] = {}
    # self.v = len(self.dag)
    return self.dag


def read_computation_costs(self):
    """q is the number of processors, n is which graph"""
    # computation_costs_ = []
    filename = 'save_dag' + '/' + 'new/v=' + str(self.v) + 'q=' + str(self.Q) + '/_' + str(self.n) \
               + '_computation_costs_q=' + str(self.Q) + '.txt'
    with open(filename, 'r') as file_object:
        lines = file_object.readlines()
        for line in lines:
            line_list = line.split()
            temp_list = []
            for i in range(len(line_list)):
                temp_list.append(int(line_list[i]))
            # computation_costs_.append(temp_list)
            self.computation_costs.append(temp_list)
    return self.computation_costs
