import random
from copy import copy, deepcopy


def get_0_or_1():
    chance = int(random.random() * 100)
    return 1 if chance % 2 == 0 else 0


def pls_clone_correctly(indiv):
    return deepcopy(indiv)
