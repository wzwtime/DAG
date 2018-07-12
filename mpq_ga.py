# coding=utf
"""Multiple Priority Queues Genetic Algorithm (MPQGA)"""
import init_population
import copy
import heft_new
import random


class MPQGA:

    def __init__(self, popsize):
        self.PopSize = popsize      # Population size
        self.Poputation = []
        self.NextPoputation = []
        self.Pc = 0.1       # Probability of crossover operator occurrence
        self.Pm = 0.01      # Probability of mutation operator occurrence
        self.G = 2          # An algebra that terminates evolution
        self.fitness = []

    def task_to_processor_mapping_fitness(self, q_, n_, v_):
        max_makespan = 0
        makespan = []
        for t in range(self.PopSize):
            rank_u = self.Poputation[t]
            new_rank = []
            # print(rank_u)
            for item in range(v_):
                temp_rank = [rank_u[item], 0]
                new_rank.append(temp_rank)
            # print("t =", t, "new_rank_u =", new_rank)
            heft = heft_new.Heft(q_, n_, v_, new_rank)
            heft_make_span = heft.heft()
            if max_makespan < heft_make_span:
                max_makespan = heft_make_span
            makespan.append(heft_make_span)
        # print("max_makespan =", max_makespan)
        # print("makespan =", makespan)
        """evaluate the fitness (makespan)"""
        for m in range(self.PopSize):
            self.fitness.append(max_makespan - makespan[m] + 1)

    def calculation_pi_and_si(self):
        p_i = []
        s_i = []
        sum_fitness = sum(self.fitness)
        for p in range(self.PopSize):
            p_i.append(round(self.fitness[p] / sum_fitness, 4))
            s_i.append(round(sum(p_i), 4))
        # print("p_i =", p_i)
        # print("s_i =", s_i)
        return s_i

    def selection(self, s_i):
        for i in range(self.PopSize - 1):  # Choose how many
            r = round(random.random(), 4)
            for k in range(self.PopSize):
                if s_i[k] > r:
                    # print("k =", k, "r =",  r)
                    self.NextPoputation.append(self.Poputation[k])
                    break

    def mpqga(self, v_, q_, n_):
        """main"""
        init_ppl = init_population.InitPopulation(self.PopSize, v_, q_, n_)
        self.Poputation = copy.deepcopy(init_ppl.get_init_population())

        g = 1
        while g <= self.G:
            self.NextPoputation = []
            self.fitness = []
            """perform task-to-processor mapping and evaluate the fitness (makespan)"""

            self.task_to_processor_mapping_fitness(q_, n_, v_)

            """Copy the elitism directly to the next new population"""
            elitism = copy.deepcopy(self.Poputation[self.fitness.index(max(self.fitness))])
            self.NextPoputation.append(elitism)

            print("------------------------------------------")
            print("fitness =", self.fitness)
            print("NextPoputation =", self.NextPoputation)

            """Calculation p_i and S_i"""
            s_i = self.calculation_pi_and_si()

            """selection"""
            self.selection(s_i)

            print("NextPoputation =", self.NextPoputation)
            print("len(self.NextPoputation) =", len(self.NextPoputation))

            """crossover"""
            p_index = [i for i in range(int(self.PopSize))]
            random.shuffle(p_index)
            print(p_index)
            for p in range(0, int(self.PopSize), 2):
                p1_index = p_index[p]
                p2_index = p_index[p + 1]
                p1 = self.NextPoputation[p1_index]
                p2 = self.NextPoputation[p2_index]
                print(p1_index, p2_index, p1, p2)
                """Choose randomly a suitable crossover point i"""


            """mutation"""

            """Replace the old population by the new population"""
            self.Poputation = copy.deepcopy(self.NextPoputation)

            g += 1


if __name__ == "__main__":
    v = 8
    q = 3
    n = 1
    PopSize = 2 * v
    mpq_ga = MPQGA(PopSize)
    mpq_ga.mpqga(v, q, n)

