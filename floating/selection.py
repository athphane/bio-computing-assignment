from random import randint
from floating.individual import Individual
from copy import deepcopy


class Selection:
    def __init__(self):
        pass

    def tournamentSelection(self, population):
        # selection_1 = population[randint(0, len(population)) - 1]
        # selection_2 = population[randint(0, len(population)) - 1]

        selection_1: Individual = population[randint(0, len(population)) - 1]
        selection_2: Individual = population[randint(0, len(population)) - 1]

        if selection_1.getFitness() > selection_2.getFitness():
            return deepcopy(selection_1)
        else:
            return deepcopy(selection_2)

