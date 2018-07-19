# coding=utf-8
import heft_new
import cpop_new
import peft
import random
import operator
import copy


class InitPopulation:

    def __init__(self, popsize, v_, q_, n_):
        self.init_individuals = []
        self.Population = []

        """HEFT"""
        self.heft = heft_new.Heft(q_, n_, v_, 0)
        self.computation_costs = self.heft.computation_costs
        self.dag = self.heft.dag
        self.heft_make_span = self.heft.heft()
        self.pred = self.heft.pred
        self.Blevel = self.heft.Blevel
        self.init_individuals.append(self.Blevel)
        self.Population.append(self.Blevel)
        """CPOP"""
        self.cpop = cpop_new.Cpop(q_, n_, v_)
        self.cpop_make_span = self.cpop.cpop()
        self.Llevel = self.cpop.Llevel
        self.init_individuals.append(self.Llevel)
        self.Population.append(self.Llevel)
        """PEFT"""
        self.peft = peft.Peft(v_, q_, n_,)
        self.peft_make_span = self.peft.peft()
        self.Tlevel = self.peft.Tlevel
        self.init_individuals.append(self.Tlevel)
        self.Population.append(self.Tlevel)

        self.v = v_

        self.PopSize = popsize
        self.PopulationN = 3

    def judge(self, tem_individual):
        # Judge whether the tem_individual is satisfied the tabu list
        count = 0
        for index in range(1, self.v - 1):
            job = tem_individual[index]
            job_pred = self.pred[job - 1][1]
            num = 0
            for m in range(index):
                if tem_individual[m] in job_pred:
                    num += 1
            if num == len(job_pred):
                count += 1
        if count == self.v - 2:
            self.Population.append(tem_individual)
            self.PopulationN += 1
            # print("Yes! self.PopulationN =", self.PopulationN)

    def add_temp_individual(self, t, label):
        """Add the temporary individual to the Population """
        for i in range(1, self.v - 1):
            if label == "init":
                tem_individual = copy.deepcopy(self.init_individuals[t])
            else:
                tem_individual = copy.deepcopy(self.Population[t])
            # print("------------------------------------------")
            # print("tem_individual =", tem_individual)
            ti = tem_individual[i]
            # print("ti =", ti)
            # print("i =", i)
            """find the last predecessor Tj of Pred(i) (i=2,3,4...v) in the tem_individual"""
            self.pred.sort(key=operator.itemgetter(0), reverse=False)
            tj = self.pred[ti - 1][1][-1]
            # print("tj =", tj)
            j = tem_individual.index(tj)
            # print("j =", j)

            """find the first successor Tk of Succ(i) in the tem_individual"""
            if len(self.dag[ti]):
                tk = list(self.dag[ti].keys())[0]
                # print("tk =", tk)
                k = tem_individual.index(tk)
                # print("k =", k)
                temp = ti

                if (k - i) > (i - j):
                    l = k - 1
                    # print("l =", l)
                    for q in range(i, k - 1):
                        tem_individual[q] = tem_individual[q + 1]
                else:
                    l = j + 1
                    # print("l =", l)
                    q = i
                    while q > j + 1:
                        tem_individual[q] = tem_individual[q - 1]
                        q = q - 1
                # tl = temp
                tem_individual[l] = temp
                # print("new individual =", tem_individual)

                # Judge whether the tem_individual is satisfied the tabu list
                self.judge(tem_individual)

                if self.PopulationN == self.PopSize:
                    break

    def get_init_population(self):
        """get 3(n -1) + 3 = 3n individuals"""
        label = "init"
        for t in range(3):
            """Add the temporary individual to the Population """
            self.add_temp_individual(t, label)

        while self.PopulationN < self.PopSize:
            index = random.randint(0, self.PopulationN - 1)
            label = "others"
            self.add_temp_individual(index, label)
        # print("self.PopulationN =", self.PopulationN)
        # print("Population =", self.Population)
        return self.Population


if __name__ == "__main__":
    v = 20
    q = 7
    n = 23
    PopSize = 2 * v
    init_ppl = InitPopulation(PopSize, v, q, n)
    print("Blevel(HEFT) =", init_ppl.Blevel)
    print("Llevel(CPOP) =", init_ppl.Llevel)
    print("Tlevel(PEFT) =", init_ppl.Tlevel)
    print("init_individuals =", init_ppl.init_individuals)
    print("Population =", init_ppl.Population)
    init_ppl.get_init_population()
    print("PopSize =", len(init_ppl.Population))




