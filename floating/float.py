from copy import deepcopy
from typing import List

from floating.crossover import Crossover
from floating.individual import Individual
from floating.selection import Selection

POPULATION_SIZE = 200
CHROMOSOME_LENGTH = 20
GENE_SIZE = 20
MUTATION_RATE = 0.01
OMEGA_OFFSET_FIXED = 0.3
NUMBER_OF_GENERATIONS = 30000


class FloatGA:
    def __init__(self):
        self.population = None
        self.dataset = None
        self.training_set = None
        self.testing_set = None

        self.CONDITION_LENGTH = 0
        self.OUTPUT_LENGTH = 0

        self.parentPopulation: List[Individual] = []
        self.offspringPopulation = []
        self.bestIndividual = None
        self.worstIndividual = None

    def readFile(self):
        """
        Read the dataset file and load it into the self.dataset variable.
        :return:
        """
        file = open('data/data3.txt', 'r')
        lines = file.readlines()

        conditionLengthTemp = 0
        outputLengthTemp = 0

        # This is the raw data that is read from the dataset file.
        datasetAL = []

        # This section creates each set, meaning each row of the dataset is
        # split by the blank space and loaded as lists.
        for line in lines:
            data = line.strip().split(' ')

            # Measure condition length and output length here
            if conditionLengthTemp == 0:
                conditionLengthTemp = len(data) - 1

            if outputLengthTemp == 0:
                outputLengthTemp = 1

            set = []

            # Loop and append without the last element.
            for i, x in enumerate(data[:-1]):
                set.append(float(x))

            # Add the last element
            set.append(float(data[len(data) - 1]))

            datasetAL.append(set)

        # Here I zerofill the dataset so that when I run loops I will have the
        # indices already filled. This will prevent index out of range errors.
        self.dataset = [[0] * (conditionLengthTemp + outputLengthTemp) for _ in range(len(datasetAL))]

        # Loop the zerofill class dataset and load up the raw data into the dataset.
        for i in range(len(self.dataset)):
            for j in range(len(self.dataset[i])):
                self.dataset[i][j] = datasetAL[i][j]

        # Set the calculated condition length and output length into the class variables.
        self.CONDITION_LENGTH = conditionLengthTemp
        self.OUTPUT_LENGTH = outputLengthTemp

    def initializeDataset(self):
        """
        Zerofill the training set and testing set
        :return:
        """
        self.training_set = [[0] * (self.CONDITION_LENGTH + self.OUTPUT_LENGTH) for _ in range(1000)]
        self.testing_set = [[0] * (self.CONDITION_LENGTH + self.OUTPUT_LENGTH) for _ in range(1000)]

        i = 0

        # Load up the first half of the large dataset into the training set.
        while i < len(self.dataset) / 2:
            self.training_set[i] = self.dataset[i]
            i += 1

        # Load up the other half of the dataset into the testing set.
        while i < len(self.dataset):
            self.testing_set[i % len(self.training_set)] = self.dataset[i]
            i += 1

    def init_populations(self):
        """
        Again, zerofill parent and offspring populations.
        And then create Individual objects for the whole range.
        :return:
        """
        self.parentPopulation = [0 for _ in range(POPULATION_SIZE)]
        self.offspringPopulation = [0 for _ in range(POPULATION_SIZE)]

        for i in range(POPULATION_SIZE):
            self.parentPopulation[i] = Individual(CHROMOSOME_LENGTH, self.CONDITION_LENGTH, self.OUTPUT_LENGTH)
            self.offspringPopulation[i] = Individual(CHROMOSOME_LENGTH, self.CONDITION_LENGTH, self.OUTPUT_LENGTH)

        # Set the best individual as a new Individual object
        # Overwritten later in the algorithm
        self.bestIndividual = Individual(CHROMOSOME_LENGTH, self.CONDITION_LENGTH, self.OUTPUT_LENGTH)

    def generateOffspring(self):
        """
        Runs the selection and crossover.
        :return:
        """
        for x in range(len(self.offspringPopulation)):
            # Selection
            parents = [
                Selection().tournament_selection(self.parentPopulation),
                Selection().tournament_selection(self.parentPopulation)
            ]

            # Crossover
            children = Crossover().run(parents[0], parents[1], GENE_SIZE)

            # Mutation and add offspring to population for the first child
            children[0].mutation_control(MUTATION_RATE, OMEGA_OFFSET_FIXED)
            children[0].mutation_output(MUTATION_RATE)
            self.offspringPopulation[x] = children[0]

            # Setup for the offspring population as well.
            if x + 1 < len(self.offspringPopulation):
                x += 1

                # Mutation and add offspring to population for the second child
                children[1].mutation_control(MUTATION_RATE, OMEGA_OFFSET_FIXED)
                children[1].mutation_output(MUTATION_RATE)
                self.offspringPopulation[x] = children[1]

        # Find and set best and worst individuals.
        self.get_best_individual()
        self.get_worst_individual()

    def copy_children_to_parents(self):
        """
        Copies the updated offspring population into the parent population
        using deepcopy for new objects with no references.
        :return:
        """
        for i, x in enumerate(self.parentPopulation):
            self.parentPopulation[i] = deepcopy(self.offspringPopulation[i])

    def get_best_individual(self):
        """
        Loop through entire offspring population and find the one with the best fitness

        Set the best individual using deepcopy with no references.
        :return:
        """
        bestFitnessIndex = 0

        for i, x in enumerate(self.offspringPopulation):
            if x.getFitness() > self.offspringPopulation[bestFitnessIndex].getFitness():
                bestFitnessIndex = i

        self.bestIndividual = deepcopy(self.offspringPopulation[bestFitnessIndex])

    def get_worst_individual(self):
        """
        Loop through entire offspring population and find the one with the worst fitness

        Set the worst individual using deepcopy with no references.
        :return:
        """
        worstFitnessIndex = 0

        for i, x in enumerate(self.offspringPopulation):
            if x.getFitness() < self.offspringPopulation[worstFitnessIndex].getFitness():
                worstFitnessIndex = i

        self.worstIndividual = deepcopy(self.offspringPopulation[worstFitnessIndex])


if __name__ == '__main__':
    # Float GA class instance
    ga = FloatGA()

    # Read the data file and init datasets.
    ga.readFile()
    ga.initializeDataset()

    # ga.newCSV()

    # Zerofill the populations
    ga.init_populations()

    # Current number of generations
    current_generation = 0

    # Because of the large dataset, we will be switching from training to testing.
    # This variable will handle the references to that.
    running_dataset = ga.dataset

    # Main application logic
    while current_generation < NUMBER_OF_GENERATIONS:

        # Switch datasets every 10 generations
        if current_generation % 10 == 0:
            running_dataset = ga.testing_set
            print("Using TESTING set now")
        else:
            running_dataset = ga.training_set
            print("Using TRAINING set now")

        # Run fitness function on parents
        for i, x in enumerate(ga.parentPopulation):
            x.evaluate(running_dataset)

        # Generate offspring
        ga.generateOffspring()

        print(f"Best Fitness: {ga.bestIndividual.getFitness()} | Generations: {current_generation}")

        # CSV goes here

        # Copy children to parents
        ga.copy_children_to_parents()

        current_generation += 1
