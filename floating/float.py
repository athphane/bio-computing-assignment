from copy import deepcopy
from floating.individual import Individual
from floating.crossover import Crossover
from floating.selection import Selection
from typing import List
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
        file = open('data/data3.txt', 'r')
        lines = file.readlines()

        conditionLengthTemp = 0
        outputLengthTemp = 0
        datasetAL = []

        # Create sets
        for line in lines:
            data = line.strip().split(' ')

            if conditionLengthTemp == 0:
                conditionLengthTemp = len(data) - 1

            if outputLengthTemp == 0:
                outputLengthTemp = 1

            set = []

            for i, x in enumerate(data[:-1]):
                set.append(float(x))

            set.append(float(data[len(data) - 1]))

            datasetAL.append(set)

        # TODO: Look into this more.
        # Populate datasets
        # Zerofill the array
        self.dataset = [[0] * (conditionLengthTemp + outputLengthTemp) for _ in range(len(datasetAL))]
        for i in range(len(self.dataset)):
            for j in range(len(self.dataset[i])):
                self.dataset[i][j] = datasetAL[i][j]

        self.CONDITION_LENGTH = conditionLengthTemp
        self.OUTPUT_LENGTH = outputLengthTemp

    def initializeDataset(self):
        self.training_set = [[0] * (self.CONDITION_LENGTH + self.OUTPUT_LENGTH) for _ in range(1000)]
        self.testing_set = [[0] * (self.CONDITION_LENGTH + self.OUTPUT_LENGTH) for _ in range(1000)]

        i = 0

        while i < len(self.dataset) / 2:
            self.training_set[i] = self.dataset[i]
            i += 1

        while i < len(self.dataset):
            self.testing_set[i % len(self.training_set)] = self.dataset[i]
            i += 1

    def initializedPopulations(self):
        self.parentPopulation = [0 for _ in range(POPULATION_SIZE)]
        self.offspringPopulation = [0 for _ in range(POPULATION_SIZE)]

        for i in range(POPULATION_SIZE):
            self.parentPopulation[i] = Individual(CHROMOSOME_LENGTH, self.CONDITION_LENGTH, self.OUTPUT_LENGTH)
            self.offspringPopulation[i] = Individual(CHROMOSOME_LENGTH, self.CONDITION_LENGTH, self.OUTPUT_LENGTH)

        # set best individual
        self.bestIndividual = Individual(CHROMOSOME_LENGTH, self.CONDITION_LENGTH, self.OUTPUT_LENGTH)

    def generateOffspring(self, running_dataset):
        for x in range(len(self.offspringPopulation)):

            # Selection
            parents = [
                Selection().tournamentSelection(self.parentPopulation),
                Selection().tournamentSelection(self.parentPopulation)
            ]

            # Crossover
            children = Crossover().singlePointCrossover(parents[0], parents[1], GENE_SIZE)

            children[0].mutationCreepConditions(MUTATION_RATE, OMEGA_OFFSET_FIXED)
            children[0].mutationOutput(MUTATION_RATE)
            self.offspringPopulation[x] = children[0]

            if x + 1 < len(self.offspringPopulation):
                x += 1
                children[1].mutationCreepConditions(MUTATION_RATE, OMEGA_OFFSET_FIXED)
                children[1].mutationOutput(MUTATION_RATE)
                self.offspringPopulation[x] = children[1]

        self.getBestIndividualNoSort()
        self.getWorstIndividualNoSort()

    def copyChildrenToParents(self):
        for i, x in enumerate(self.parentPopulation):
            self.parentPopulation[i] = deepcopy(self.offspringPopulation[i])

    def getBestIndividualNoSort(self):
        bestFitnessIndex = 0

        for i, x in enumerate(self.offspringPopulation):
            if x.getFitness() > self.offspringPopulation[bestFitnessIndex].getFitness():
                bestFitnessIndex = i

        self.bestIndividual = deepcopy(self.offspringPopulation[bestFitnessIndex])

    def getWorstIndividualNoSort(self):
        worstFitnessIndex = 0

        for i, x in enumerate(self.offspringPopulation):
            if x.getFitness() < self.offspringPopulation[worstFitnessIndex].getFitness():
                worstFitnessIndex = i

        self.worstIndividual = deepcopy(self.offspringPopulation[worstFitnessIndex])


if __name__ == '__main__':
    ga = FloatGA()
    ga.readFile()
    ga.initializeDataset()
    # ga.newCSV()
    ga.initializedPopulations()

    print("Hello")

    number_of_generations = 0

    running_dataset = ga.dataset

    while number_of_generations < NUMBER_OF_GENERATIONS:
        parentPopulationSorted = False
        offspringPopulationSorted = False

        # Switch datasets every 10 generations
        if number_of_generations % 10 == 0:
            running_dataset = ga.testing_set
            print("Using TESTING set now")
        else:
            running_dataset = ga.training_set
            print("Using TRAINING set now")

        # Run fitness function on parents
        for i, x in enumerate(ga.parentPopulation):
            x.evaluate(running_dataset)

        # Generate offspring
        ga.generateOffspring(running_dataset)

        print(f"Best Fitness: {ga.bestIndividual.getFitness()} | Generations: {number_of_generations}")

        # CSV goes here

        # Copy children to parents
        ga.copyChildrenToParents()

        number_of_generations += 1
