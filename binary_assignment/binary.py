from Population import Population


class BinaryGA:
    def __init__(self):
        self.population = Population(None, 7)
        self.dataset = None

    def read_data_file(self):
        """
        Load up the data files
        :return:
        """
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
        """
        Function to help convert the input string to integer list
        :param data:
        :return:
        """
        temp_arr = []
        for x in data:
            for y in x:
                temp_arr.append(int(y))
        return temp_arr


if __name__ == '__main__':
    # Number of generations to run
    generations_count = 100

    # GA class
    ga = BinaryGA()

    # Load up the dataset from file
    ga.read_data_file()

    # CSV writer
    f = open('../output/ds2.csv', 'w')

    # The populations dataset
    ga.population.dataset = ga.dataset

    # Current generation
    current_generation = 1

    # Main application logic
    while current_generation <= generations_count:
        # The run fitness function on the population
        ga.population.run_fitness_function()

        print(f"Generation: {current_generation + 1} - Best Fitness: {ga.population.best_fitness}")

        # Save data to a file here for later analysis
        f.write(f"{ga.population.best_fitness},{ga.population.average_fitness},{ga.population.worst_fitness}\n")

        # Run selection
        ga.population.selection()

        # Run crossover
        ga.population.crossover()

        # Run mutation
        ga.population.mutation()

        # Create next generation
        ga.population.init_next_generation()

        current_generation += 1

    print("Completed")
    print(ga.population.show_best_individual())

    f.close()
