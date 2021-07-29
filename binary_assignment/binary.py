from Population import Population
import sys


class BinaryGA:
    def __init__(self):
        self.population = Population(None, 7)
        self.dataset = None

    def read_data_file(self):
        file = open('data/data2.txt', 'r')
        lines = file.readlines()

        rules = []
        count = 0
        for line in lines:
            data = line.strip().split(' ')
            rule_array = self.convert_array_to_full_int_array(data)
            rules.append(rule_array)
            count += 1

        self.dataset = rules

        print(f"{count} lines of data read")

    @staticmethod
    def convert_array_to_full_int_array(data):
        temp_arr = []
        for x in data:
            for y in x:
                temp_arr.append(int(y))
        return temp_arr


if __name__ == '__main__':
    generations_count = 100

    ga = BinaryGA()
    ga.read_data_file()

    ga.population.dataset = ga.dataset

    current_generation = 1

    while current_generation <= generations_count:
        ga.population.run_fitness_function()

        print(f"Generation: {current_generation + 1} - Best Fitness: {ga.population.best_fitness}")
        # Save data to a file here for later analysis

        ga.population.selection()

        ga.population.crossover()

        ga.population.mutation()

        ga.population.init_next_generation()

        current_generation += 1

    print("Completed")
    print(ga.population.show_best_individual())
