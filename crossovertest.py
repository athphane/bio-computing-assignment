import random

p1 = [0, 1, 2, 3, 4]
p2 = [0, 0, 0, 0, 0]


def crossover(input1, input2):
    k = random.randint(0, len(input1) - 1)
    print(f"Crossing Point: {k}")

    for x in range(k, len(input1)):
        input1[x], input2[x] = input2[x], input1[x]

    print(input1)
    print(input2)

if __name__ == '__main__':
    crossover(p1, p2)