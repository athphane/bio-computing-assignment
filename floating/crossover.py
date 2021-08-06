from copy import deepcopy
from random import randint, random
import sys
from floating.individual import Individual


class Crossover:
    def __init__(self):
        pass

    def singlePointCrossover(self, parent1: Individual, parent2: Individual, CROSSOVER_RATE):
        children = [None, None]

        if CROSSOVER_RATE > random():
            calc = len(parent1.getGenes()) * len(parent1.getGenes()[0])
            crossoverPosition = randint(0, calc)

            counter = 0
            i = 0

            while crossoverPosition > counter:
                mod = counter % len(parent1.getGenes()[0])

                if mod == len(parent1.getGenes()[0]) - 1:
                    i += 1

                try:
                    temp = parent1.getGenes()[i][mod]
                    parent1.setGeneFromIndex(i, mod, parent2.getGenes()[i][mod])
                    parent2.setGeneFromIndex(i, mod, temp)
                except IndexError:
                    print(f"i: {i} | mod: {mod}")

                counter += 1

        children[0] = deepcopy(parent1)
        children[1] = deepcopy(parent2)

        return children
