from binary_second_attempt.population import Population


def convert_array_to_full_int_array(data):
    temp_arr = []
    for x in data:
        for y in x:
            temp_arr.append(int(y))
    return temp_arr


def read_data_file():
    file = open('data/data1.txt', 'r')
    lines = file.readlines()

    rules = []
    count = 0
    for line in lines:
        data = line.strip().split(' ')
        rule_array = convert_array_to_full_int_array(data)
        rules.append(rule_array)
        count += 1

    print(f"{count} lines of data read")
    return rules


if __name__ == '__main__':
    generations_count = 1000

    population = Population(10, 6, 100)
    dataset = read_data_file()
    population.set_dataset(dataset)

    for current_generation in range(generations_count):
        population.fitness_function()

        print(f"Generation: {current_generation + 1} - Best Fitness: {population.best_fitness}")
        print(population.best_fitness, population.average_fitness, population.worst_fitness)
        # Save data to a file here for later analysis

        population.selection()

        population.crossover()

        population.mutation()

        population.init_next_generation()

    print("Completed")
    print(population.show_best_individual())
