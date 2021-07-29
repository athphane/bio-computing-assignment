from copy import copy
from random import choice, random



class Individual:
    def __init__(self, GENE_SIZE=10, RULE_SIZE=6, clone=None):
        self.GENE_SIZE = GENE_SIZE
        self.RULE_SIZE = RULE_SIZE
        self.genes = None
        self.fitness = 0
        self.allowed_values = [0, 1]

        if not clone:
            self.init_genes()
            self.randomize_genes()
        else:
            self.copy_gene(clone)

    def init_genes(self):
        self.genes = [[0 for _ in range(self.RULE_SIZE)] for _ in range(self.GENE_SIZE)]

    def get_genes(self):
        return self.genes

    def get_gene(self, idx):
        return self.genes[idx]

    def set_gene(self, gene_idx, idx, val):
        self.genes[gene_idx][idx] = val

    def set_gene_output(self, gene_idx, val):
        self.genes[gene_idx][len(self.genes[gene_idx] - 1)] = val

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, val):
        self.fitness = val

    def reset_fitness(self):
        self.fitness = 0

    def randomize_genes(self):
        for i, gene in enumerate(self.genes):
            for j, x in enumerate(gene[:-1]):
                self.set_gene(i, j, choice(self.allowed_values))  # randomize inputs

            self.set_gene(i, len(gene) - 1, choice(self.allowed_values))  # randomize output

    def fitness_function(self, dataset):
        self.reset_fitness()

        for i, dataset_row in enumerate(dataset):

            for j, gene in enumerate(self.genes):
                dataset_accurate = True

                for k, gene_item in enumerate(gene[:-1]):
                    if gene[k] == dataset_row[k]:
                        dataset_accurate = True
                    else:
                        dataset_accurate = False
                        break

                if dataset_accurate:
                    if gene[len(gene) - 1] == dataset_row[len(dataset_row) - 1]:
                        self.fitness += 1

                    break

    def mutation(self, mutation_rate):
        for i, gene in enumerate(self.genes):
            for j, iterm in enumerate(gene[:-1]):
                if mutation_rate > random():
                    self.genes[i][j] = choice(self.allowed_values)

            if mutation_rate > random():
                self.genes[i][len(self.genes[i]) - 1] = choice(self.allowed_values)

    def copy_gene(self, clone):
        temp_genes = clone.genes

        self.genes

        new_indiv = Individual(self.GENE_SIZE, self.RULE_SIZE, True)
        new_indiv
        return copy(self)
