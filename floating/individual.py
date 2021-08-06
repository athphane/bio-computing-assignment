import sys
from random import choice, random


class Individual:
    def __init__(self, GENE_LENGTH, CONDITION_LENGTH, OUTPUT_LENGTH):
        self.geneLength = GENE_LENGTH
        self.conditionLength = CONDITION_LENGTH
        self.outputLength = OUTPUT_LENGTH
        self.totalLength = (self.conditionLength * 2) + self.outputLength
        self.fitness = 0
        self.genes = [[0] * self.totalLength for _ in range(self.geneLength)]

        self.randomizeGenes()
        self.organizeBounds()

    def randomizeGenes(self):
        for i in range(len(self.genes)):
            for j in range(len(self.genes[i])):
                if j == len(self.genes[i]) - 1:
                    self.genes[i][j] = choice([0, 1, 2])
                else:
                    self.genes[i][j] = random()

    def organizeBounds(self):
        for i in range(len(self.genes)):
            for j in range(int((len(self.genes[i]) - self.outputLength) / 2)):
                offset = j * 2

                lowerBound = min(self.genes[i][offset], self.genes[i][offset + 1])
                upperBound = max(self.genes[i][offset], self.genes[i][offset + 1])

                self.genes[i][offset] = lowerBound
                self.genes[i][offset + 1] = upperBound

    def evaluate(self, dataset):
        tempFitness = 0

        for i in range(len(dataset)):
            fs = dataset[i]

            for j in range(len(self.genes)):
                allMatched = True

                for k in range(len(fs) - self.outputLength):
                    value = fs[k]
                    offset = k * 2

                    lowerBound = self.genes[j][offset]
                    upperBound = self.genes[j][offset + 1]

                    if not ((lowerBound <= value) and (value <= upperBound)):
                        allMatched = False
                        break

                if allMatched:
                    if self.genes[j][self.totalLength - 1] == fs[len(fs) - 1]:
                        tempFitness += 1

                    break

        self.fitness = tempFitness

    def mutationCreepConditions(self, MUTATION_RATE, OMEGA_OFFSET):
        for i in range(len(self.genes)):
            for j in range(self.conditionLength):
                if MUTATION_RATE > random():
                    offset = j * 2

                    lowerBound = self.genes[i][offset]
                    upperBound = self.genes[i][offset + 1]

                    lowerBound += random() * OMEGA_OFFSET if random() > 0.5 else -random() * OMEGA_OFFSET
                    upperBound += random() * OMEGA_OFFSET if random() > 0.5 else -random() * OMEGA_OFFSET

                    lowerBound = self.zero_or_one(lowerBound)
                    upperBound = self.zero_or_one(upperBound)

                    self.genes[i][offset] = min(lowerBound, upperBound)
                    self.genes[i][offset + 1] = max(lowerBound, upperBound)

    @staticmethod
    def zero_or_one(value):
        if value < 0:
            return 0

        if value > 1:
            return 1
        else:
            return value

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def setGeneFromIndex(self, i, j, val):
        self.genes[i][j] = val

    def mutationOutput(self, mutation_rate):
        for i in range(len(self.genes)):
            if mutation_rate > random():
                self.genes[i][len(self.genes[i]) - 1] = int(self.genes[i][len(self.genes[i]) - 1] ^ 1)

