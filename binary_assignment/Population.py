from copy import copy, deepcopy
from random import randint

from Individual import Individual
from binary_assignment.helpers import pls_clone_correctly


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
        self.population = []
        self.mating_pool = []

        self.best_fitness = 0
        self.average_fitness = 0
        self.worst_fitness = 0

        self.initialize_population()
        self.initialize_mating_pool()

        self.randomize_population_genes()

    def initialize_population(self):
        for _ in range(self.POPULATION_SIZE):
            self.population.append(Individual(self.GENE_SIZE, self.RULE_SIZE))

    def initialize_mating_pool(self):
        for _ in range(self.POPULATION_SIZE):
            self.mating_pool.append(Individual(self.GENE_SIZE, self.RULE_SIZE))
        # self.mating_pool = [None for _ in range(self.POPULATION_SIZE)]

    def randomize_population_genes(self):
        for individual in self.population:
            individual.randomize_genes()

    def run_fitness_function(self):
        """
        This is the fitness function where it measures the fitness of all the individuals of the population
        :return:
        """
        self.average_fitness = 0
        self.best_fitness = 0

        # start off worst fitness as the first Individual's fitness
        self.worst_fitness = self.population[0].get_fitness()

        temp_avg_count = 0
        for individual in self.population:
            individual.fitness_function(self.dataset)

            # Put individual's fitness into a variable
            individual_fitness = individual.get_fitness()

            # IF individual's fitness better than current best fitness
            # THEN update best fitness with current individual's
            if self.best_fitness < individual_fitness:
                self.best_fitness = individual_fitness

            # IF individual's fitness is worse than current worst fitness
            # THEN update worst fitness with current individual's
            if self.worst_fitness > individual_fitness:
                self.worst_fitness = individual_fitness

            # Add up all individuals' fitness and divide later
            self.average_fitness += individual_fitness

        self.average_fitness /= len(self.population)

    def selection(self):
        """
        This function runs the tournament selection to create a mating pool for the next generation
        :return: None
        """
        for x in range(self.POPULATION_SIZE):
            self.mating_pool[x] = self.tournament_selection()
        # for x, individual in enumerate(self.mating_pool):
        #     self.mating_pool[x] = self.tournament_selection()

    def tournament_selection(self):
        """
        This is the tournament selection function where it selects 2 random Individuals from the population and
        returns the fittest individual deterministic to their fitness values.
        :return:
        """
        selection_1 = self.population[randint(0, self.POPULATION_SIZE) - 1]
        selection_2 = self.population[randint(0, self.POPULATION_SIZE) - 1]

        mate_1: Individual = deepcopy(selection_1)
        mate_2: Individual = deepcopy(selection_2)

        if mate_1.get_fitness() > mate_2.get_fitness():
            return mate_1
        else:
            return mate_2

    # def crossover(self):
    #     """
    #     The function that handles the main crossover function
    #     :return:
    #     """
    #
    #     mating_pool_length = len(self.mating_pool)
    #     half_of_mating_pool = int(mating_pool_length / 2)
    #
    #     for i, x in enumerate(self.mating_pool[:half_of_mating_pool]):
    #         offset = i * 2
    #
    #         children = self.single_point_crossover(self.mating_pool[offset], self.mating_pool[offset + 1])
    #
    #         self.mating_pool[i] = children[0]
    #         self.mating_pool[i + 1] = children[1]

    def crossover(self):
        for i in range(int(len(self.mating_pool) / 2)):
            offset = i * 2

            children = self.single_point_crossover(self.mating_pool[offset], self.mating_pool[offset + 1])

            self.mating_pool[i] = children[0]
            self.mating_pool[i + 1] = children[1]

    def single_point_crossover(self, parent_1: Individual, parent_2: Individual):
        # child_1 = Individual(child=parent_1)
        # child_2 = Individual(child=parent_2)

        children = [
            deepcopy(parent_1),
            deepcopy(parent_2)
        ]

        # crossover_point = randint(0, self.GENE_SIZE * self.RULE_SIZE)
        crossover_point = randint(0, self.RULE_SIZE)

        pointer = 0

        for i, x in enumerate(parent_1.genes):

            for j, y in enumerate(x):

                if pointer < crossover_point:
                    temp = children[0].genes[i][j]
                    children[0].genes[i][j] = children[1].genes[i][j]
                    children[1].genes[i][j] = temp
                else:
                    break

                pointer += 1

            if pointer >= crossover_point:
                break
        # for x in range(len(parent_1.genes)):
        #     child_1_gene = child_1.genes[x]
        #     child_2_gene = child_2.genes[x]
        #
        #     for y in range(crossover_point, len(child_1_gene)):
        #         child_1_gene[y], child_2_gene[y] = child_2_gene[y], child_1_gene[y]
        #
        #     child_1.genes[x] = child_1_gene
        #     child_2.genes[x] = child_2_gene

        return children

    def mutation(self):
        for x in range(len(self.mating_pool)):
            self.mating_pool[x].mutate(self.MUTATION_RATE)

    # def mutation(self):
    #     for i, individual in enumerate(self.mating_pool):
    #         self.mating_pool[i].mutate(self.MUTATION_RATE)

    def init_next_generation(self):
        for x in range(len(self.population)):
            self.population[x] = deepcopy(self.mating_pool[x])

    # def init_next_generation(self):
    #     for i in range(self.POPULATION_SIZE):
    #         # self.population[i] = Individual(self.GENE_SIZE, self.RULE_SIZE, self.mating_pool[i])
    #         mate = self.mating_pool[i]
    #         new_mate = Individual(child=mate)
    #         self.population[i] = new_mate

    def show_best_individual(self):
        best_individual: Individual = self.population[0]

        for i, individual in enumerate(self.population):
            if individual.get_fitness() > best_individual.get_fitness():
                best_individual = self.population[i]

        print("This is the best individual")
        print(best_individual.get_genes())
