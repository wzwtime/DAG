# coding=utf
"""Multiple Priority Queues Genetic Algorithm (MPQGA)"""
import init_population
import copy
import heft_new
import random
import time


class MPQGA:

    def __init__(self, popsize):
        self.PopSize = popsize      # Population size
        self.Poputation = []
        self.NextPoputation = []
        # self.Pc = 0.1               # Probability of crossover operator occurrence
        self.Pm = 0.01              # Probability of mutation operator occurrence
        self.fitness = []
        self.dag = {}
        self.pred = []
        self.g = 1
        self.makespan = 0
        self.start_time = 0
        self.end_time = 0
        self.running_time = 0

    def judge(self, parent, parent_index):
        # Judge whether the tem_individual is satisfied the tabu list
        count = 0
        for index in range(1, len(parent) - 1):
            job = parent[index]
            job_pred = self.pred[job - 1][1]
            num = 0
            for t in range(index):
                if parent[t] in job_pred:
                    num += 1
            if num == len(job_pred):
                count += 1
        if count == len(parent) - 2:
            label = "yes"
            self.NextPoputation.pop(parent_index)
            self.NextPoputation.append(parent)
        else:
            label = "no"
        return label

    def task_to_processor_mapping_fitness(self, q_, n_, v_):
        max_makespan = 0
        makespan_ = []
        for t in range(self.PopSize):
            rank_u = self.Poputation[t]
            new_rank = []
            # print("rank_u =", rank_u)
            for item in range(v_):
                temp_rank = [rank_u[item], 0]
                new_rank.append(temp_rank)
            # print("t =", t, "rank_u =", rank_u)
            heft = heft_new.Heft(q_, n_, v_, new_rank)
            heft_make_span = heft.heft()
            if max_makespan < heft_make_span:
                max_makespan = heft_make_span
            makespan_.append(heft_make_span)
        # print("max_makespan =", max_makespan)
        self.makespan = max_makespan
        # print("makespan =", makespan)
        """evaluate the fitness (makespan)"""
        for m in range(self.PopSize):
            self.fitness.append(max_makespan - makespan_[m] + 1)

    def calculation_pi_and_si(self):
        p_i = []
        s_i = []
        sum_fitness = sum(self.fitness)
        for p in range(self.PopSize):
            p_i.append(round(self.fitness[p] / sum_fitness, 4))
            s_i.append(round(sum(p_i), 4))
        # print("p_i =", p_i)
        # print("sum(p_i) =", sum(p_i))
        # print("s_i =", s_i)
        return s_i

    def selection(self, s_i):
        """using roulette-wheel selection;"""
        for i in range(self.PopSize - 1):  # Choose how many
            # r = round(random.random(), 4)
            r = round(random.uniform(0, s_i[-1]), 4)
            for k in range(self.PopSize):
                if s_i[k] >= r:
                    # print("s_i[k] =", s_i[k], "r =",  r)
                    self.NextPoputation.append(self.Poputation[k])
                    break

    def crossover(self):
        """"""
        p_index = [i for i in range(int(self.PopSize))]
        random.shuffle(p_index)     # Disrupt the index
        # print("p_index =", p_index)
        new_offsprings = []

        for p in range(0, int(self.PopSize), 2):
            p1_index = p_index[p]
            p2_index = p_index[p + 1]
            father = self.NextPoputation[p1_index]
            mother = self.NextPoputation[p2_index]
            # print(p1_index, p2_index, father, mother)
            """Choose randomly a suitable crossover point i"""
            point_i = random.randint(2, len(father) - 2)
            # print("point_i =", point_i)

            """Generate a new offspring, namely the son;"""
            son = copy.deepcopy(father[: point_i])
            # print("son =", son)
            for m in mother:
                if m not in son:
                    son.append(m)
            # print("new son =", son)
            new_offsprings.append(son)

            """Generate a new offspring, namely the daughter;"""
            daughter = copy.deepcopy(mother[: point_i])
            # print("daughter =", daughter)
            for f in father:
                if f not in daughter:
                    daughter.append(f)
            # print("new daughter =", daughter)
            new_offsprings.append(daughter)
        self.NextPoputation = copy.deepcopy(new_offsprings)

    def mutation(self):
        """A randomly chosen chromosome."""
        label = "no"
        while label == "no":
            parent_index = random.randint(0, len(self.NextPoputation) - 1)
            parent = copy.deepcopy(self.NextPoputation[parent_index])

            ti_index = 0
            tj_index = 0
            while ti_index + 1 > tj_index - 1:
                ti_index = random.randint(1, len(parent) - 2)
                ti = parent[ti_index]
                tj = 0
                for key in self.dag[ti].keys():
                    tj = key
                    break
                tj_index = parent.index(tj)
            tk_index = random.randint(ti_index + 1, tj_index - 1)
            tk = parent[tk_index]
            tk_pred = self.pred[tk - 1][1]
            count = 0
            for tl in tk_pred:
                tl_index = parent.index(tl)
                if tl_index < ti_index:
                    count += 1
            if count == len(tk_pred):
                # print("---------------------yes--------------")

                """Generate a new offspring by interchanging gene Ti and gene Tk;"""
                parent[ti_index], parent[tk_index] = parent[tk_index], parent[ti_index]

                """Judge whether the parent is satisfied the tabu list"""
                label = self.judge(parent, parent_index)
            else:
                # print("----------no----------")
                label = "no"
        # print("After mutation len(NextPoputation)=", len(self.NextPoputation))

    def mpqga(self, v_, q_, n_, g_):
        """main"""
        self.start_time = time.time()
        init_ppl = init_population.InitPopulation(self.PopSize, v_, q_, n_)
        self.dag = init_ppl.dag
        self.pred = init_ppl.pred
        self.Poputation = copy.deepcopy(init_ppl.get_init_population())

        # g = 1
        # while g <= g_:
        while sum(self.fitness) != self.PopSize:
            self.NextPoputation = []
            self.fitness = []

            """perform task-to-processor mapping and evaluate the fitness (makespan)"""
            self.task_to_processor_mapping_fitness(q_, n_, v_)

            """Copy the elitism directly to the next new population"""
            elitism = copy.deepcopy(self.Poputation[self.fitness.index(max(self.fitness))])
            self.NextPoputation.append(elitism)

            # print("------------------------------------------", " g =", self.g)
            # print("fitness =", self.fitness)
            # print("makespan =", self.makespan)
            # print("NextPoputation =", self.NextPoputation)

            """Calculation p_i and S_i"""
            s_i = self.calculation_pi_and_si()

            """selection"""
            self.selection(s_i)

            # print("selection NextPoputation =", self.NextPoputation)
            # print("After selection len(NextPoputation) =", len(self.NextPoputation))

            """Crossover operator"""
            self.crossover()

            # print("Crossover NextPoputation =", self.NextPoputation)
            # print("After crossover len(NextPoputation) =", len(self.NextPoputation))

            """mutation operator"""
            self.mutation()

            # print("Mutation NextPoputation =", self.NextPoputation)
            """Replace the old population by the new population"""
            self.Poputation = copy.deepcopy(self.NextPoputation)

            self.g += 1
            # g += 1

        self.end_time = time.time()
        self.running_time = int(round((self.end_time - self.start_time), 3) * 1000)

        return self.makespan


if __name__ == "__main__":
    v = 20
    q = 7
    n = 28
    g = 50           # An algebra that terminates evolution
    PopSize = 2 * v
    for m in range(1, 2):
        mpq_ga = MPQGA(PopSize)
        makespan = mpq_ga.mpqga(v, q, n, g)
        print("Poputation = ", mpq_ga.Poputation)
        print("makespan(GA) =", makespan)
        print("G =", mpq_ga.g - 1)


