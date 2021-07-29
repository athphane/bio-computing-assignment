from typing import List
from random import randint
from binary_second_attempt.individual import Individual
import sys

class Population:
    def __init__(self, GENE_SIZE=None, RULE_SIZE=None, POPULATION_SIZE=1000, MUTATION_RATE=0.02):
        # Hyper parameters
        self.GENE_SIZE = GENE_SIZE or 10
        self.RULE_SIZE = RULE_SIZE or 6
        self.POPULATION_SIZE = POPULATION_SIZE
        self.MUTATION_RATE = MUTATION_RATE

        # Global parameters
        self.dataset = None

        # Local parameters
        self.population: List[Individual] = []
        self.mating_pool: List[Individual] = []

        self.best_fitness = 0
        self.average_fitness = 0
        self.worst_fitness = 0

        self.initialize_population()
        self.initialize_mating_pool()

        self.set_population()

    def initialize_population(self):
        for _ in range(self.POPULATION_SIZE):
            self.population.append(Individual(self.GENE_SIZE, self.RULE_SIZE))

    def initialize_mating_pool(self):
        pass

    def set_population(self):
        for indiv in self.population:
            indiv.randomize_genes()

    def set_dataset(self, dataset):
        self.dataset = dataset

    def get_mating_pool_individual(self, idx):
        return self.mating_pool[idx]

    def set_mating_pool_individual(self, idx, val):
        self.mating_pool[idx] = val

    def reset_best_avg_worst(self):
        self.best_fitness = 0
        self.average_fitness = 0
        self.worst_fitness = 0

    def fitness_function(self):
        self.reset_best_avg_worst()
        self.worst_fitness = self.population[0].get_fitness()

        for i, indiv in enumerate(self.population):
            # print(indiv.get_fitness())
            indiv.fitness_function(self.dataset)
            # print(indiv.get_fitness())
            # sys.exit()

            if self.best_fitness < indiv.get_fitness():
                self.best_fitness = indiv.get_fitness()

            if self.worst_fitness > indiv.get_fitness():
                self.worst_fitness = indiv.get_fitness()

            self.average_fitness += indiv.get_fitness()

        self.average_fitness /= len(self.population)

    def selection(self):
        for _ in range(self.POPULATION_SIZE):
            new_mating_individual = self.tournament_selection()
            self.mating_pool.append(new_mating_individual)

    def get_random_indiv(self):
        return self.population[randint(0, self.POPULATION_SIZE - 1)].copy_gene()

    def tournament_selection(self):
        random_one = self.get_random_indiv()
        random_two = self.get_random_indiv()

        if random_one.get_fitness() > random_two.get_fitness():
            return random_one
        else:
            return random_two

    def crossover(self):
        half = int(len(self.mating_pool) / 2)
        for i, indiv in enumerate(self.mating_pool[:half]):
            offset = i * 2

            indiv_1 = self.get_mating_pool_individual(offset)
            indiv_2 = self.get_mating_pool_individual(offset + 1)
            children = self.single_point_crossover(indiv_1, indiv_2)

            self.set_mating_pool_individual(i, children[0])
            self.set_mating_pool_individual(i + 1, children[1])

    def single_point_crossover(self, p1: Individual, p2: Individual):
        children = [
            p1.copy_gene(),
            p2.copy_gene()
        ]

        crossing_point = randint(0, (self.GENE_SIZE * self.RULE_SIZE) - 1)

        pointer = 0

        for i, gene in enumerate(p1.genes):
            for j, item in enumerate(gene):

                if pointer < crossing_point:
                    temp = children[0].genes[i][j]
                    children[0].genes[i][j] = children[1].genes[i][j]
                    children[1].genes[i][j] = temp
                else:
                    break

                pointer += 1

            if pointer >= crossing_point:
                break

        return children

    def mutation(self):
        for x in self.mating_pool:
            x.mutation(self.MUTATION_RATE)

    def init_next_generation(self):
        for x in range(self.POPULATION_SIZE):
            self.population[x] = self.mating_pool[x].copy_gene()

    def show_best_individual(self):
        pass



