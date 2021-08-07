from copy import deepcopy
from random import randint

from floating.individual import Individual


class Selection:
    def __init__(self):
        pass

    @staticmethod
    def tournament_selection(population):
        """
        Return deepcopy of the best individual in terms of fitness
        :param population:
        :return:
        """
        # Get two individuals randomly from the population.
        selection_1: Individual = population[randint(0, len(population)) - 1]
        selection_2: Individual = population[randint(0, len(population)) - 1]

        # Return the best
        if selection_1.getFitness() > selection_2.getFitness():
            return deepcopy(selection_1)
        else:
            return deepcopy(selection_2)
