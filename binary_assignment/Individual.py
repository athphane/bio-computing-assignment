from random import random, randint, choice
import sys
from helpers import get_0_or_1
from copy import copy


class Individual:
    def __init__(self, gene_size=None, rule_size=None):
        self.genes = [[0 for _ in range(rule_size)] for _ in range(gene_size)]
        self.fitness = 0

    def get_genes(self):
        return self.genes

    def get_fitness(self):
        return self.fitness

    def randomize_genes(self):
        for i in range(len(self.genes)):
            for j in range(len(self.genes[i]) - 1):
                self.genes[i][j] = choice([0, 1, 2])

            self.genes[i][len(self.genes[i]) - 1] = choice([0, 1, 2])

    # def randomize_genes(self):
    #     for x, gene in enumerate(self.genes):
    #         for bit_idx, bit in enumerate(gene[:-1]):
    #             self.genes[x][bit_idx] = choice([0, 1, 2])
    #
    #         self.genes[x][len(gene) - 1] = choice([0, 1])


    def fitness_function(self, dataset):
        self.fitness = 0

        # Foreach item in dataset
        for i, item in enumerate(dataset):

            # foreach gene in genes
            for j, gene in enumerate(self.genes):
                matches_conditions_from_dataset = True

                # foreach bit in gene
                for k, bit in enumerate(gene[:-1]):
                    if gene[k] == item[k] or gene[k] == 2:
                        matches_conditions_from_dataset = True
                    else:
                        matches_conditions_from_dataset = False
                        break

                if matches_conditions_from_dataset:
                    if gene[-1] == item[-1]:
                        self.fitness += 1

                    break

    def mutate(self, rate):
        for gene_id, gene in enumerate(self.genes):
            for bit_id, bit in enumerate(gene[:-1]):
                if rate > random():
                    self.genes[gene_id][bit_id] = choice([0, 1, 2])

            if rate > random():
                self.genes[gene_id][len(gene) - 1] = choice([0, 1])
