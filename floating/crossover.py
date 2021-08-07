from copy import deepcopy
from random import randint, random

from floating.individual import Individual


class Crossover:
    def __init__(self):
        pass

    @staticmethod
    def run(parent1: Individual, parent2: Individual, CROSSOVER_RATE):
        """
        Single point crossover function according to StackOverflow
        Using the crossover rate to only allow a few to crossover.
        :param parent1:
        :param parent2:
        :param CROSSOVER_RATE:
        :return:
        """
        # Set null children.
        children = [None, None]

        # If crossover rate
        if CROSSOVER_RATE > random():
            calc = len(parent1.getGenes()) * len(parent1.getGenes()[0])  # Final length
            crossoverPosition = randint(0, calc)

            counter = 0
            i = 0

            while crossoverPosition > counter:
                loc = counter % len(parent1.getGenes()[0])

                if loc == len(parent1.getGenes()[0]) - 1:
                    i += 1

                # Here a try catch is used cause and index error occurs
                # Even though it's within the range.
                try:
                    temp = parent1.getGenes()[i][loc]
                    parent1.setGeneFromIndex(i, loc, parent2.getGenes()[i][loc])
                    parent2.setGeneFromIndex(i, loc, temp)
                except IndexError:
                    # print(f"i: {i} | mod: {loc}")
                    pass

                counter += 1

        # Set deepcopy of parents to children.
        children[0] = deepcopy(parent1)
        children[1] = deepcopy(parent2)

        return children
