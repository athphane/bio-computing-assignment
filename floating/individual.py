from random import choice, random


class Individual:
    def __init__(self, GENE_LENGTH, INPUT_PARAM_LENGTH, OUTPUT_LENGTH):
        self.geneLength = GENE_LENGTH
        self.input_param_length = INPUT_PARAM_LENGTH
        self.output_length = OUTPUT_LENGTH
        self.total_length = (self.input_param_length * 2) + self.output_length
        self.fitness = 0
        self.genes = [[0] * self.total_length for _ in range(self.geneLength)]

        self.randomize_genes()
        self.organize_bounds()

    def randomize_genes(self):
        """
        Randomly assign values to the genes. Similarly done in dataset one and two
        :return:
        """
        for i in range(len(self.genes)):
            for j in range(len(self.genes[i])):
                if j == len(self.genes[i]) - 1:
                    self.genes[i][j] = choice([0, 1, 2])  # Set int for output
                else:
                    self.genes[i][j] = random()  # set random float for all inputs

    def organize_bounds(self):
        """
        Overall this function helps to find min and max of the the genes in question
        and in a sense, orders them.

        This organization is then used in the evaluation of the individual

        A tip from a colleague.
        :return:
        """
        for i in range(len(self.genes)):
            for j in range(int((len(self.genes[i]) - self.output_length) / 2)):
                offset = j * 2

                lowerBound = min(self.genes[i][offset], self.genes[i][offset + 1])
                upperBound = max(self.genes[i][offset], self.genes[i][offset + 1])

                self.genes[i][offset] = lowerBound
                self.genes[i][offset + 1] = upperBound

    def evaluate(self, dataset):
        """
        Calculate the fitness score of the individual.

        Loop through all the genes and check if the input parameters pass the
        upper bound and lower bound check.
        :param dataset:
        :return:
        """
        tempFitness = 0

        for i in range(len(dataset)):  # The whole dataset.
            fs = dataset[i]

            for j in range(len(self.genes)):  # All the genes.
                all_rules_matched = True

                for k in range(len(fs) - self.output_length):
                    value = fs[k]
                    offset = k * 2

                    # Bring back the lower bound and upper bound as variables.
                    lowerBound = self.genes[j][offset]
                    upperBound = self.genes[j][offset + 1]

                    # Condition checkpoint
                    # Break loop if not True
                    if not ((lowerBound <= value) and (value <= upperBound)):
                        all_rules_matched = False
                        break

                # If all rules match, then score fitness using gene and input dataset.
                if all_rules_matched:
                    if self.genes[j][self.total_length - 1] == fs[len(fs) - 1]:
                        tempFitness += 1

                    break

        # Set Individual fitness into class variable.
        self.fitness = tempFitness

    def mutation_control(self, mutation_rate, control_offset):
        """
        This function basically takes the float values and then applies
        and offset to make sure it is within the correct range.
        :param mutation_rate: 
        :param control_offset: 
        :return: 
        """
        for i in range(len(self.genes)):  # For all the genes
            for j in range(self.input_param_length):  # Only for all the input params
                if mutation_rate > random():
                    offset = j * 2

                    lowerBound = self.genes[i][offset]
                    upperBound = self.genes[i][offset + 1]

                    # Correct bounds
                    lowerBound += random() * control_offset if random() > 0.5 else -random() * control_offset
                    upperBound += random() * control_offset if random() > 0.5 else -random() * control_offset

                    # Set to zero or null
                    lowerBound = self.zero_or_one(lowerBound)
                    upperBound = self.zero_or_one(upperBound)

                    # Set the min and max
                    self.genes[i][offset] = min(lowerBound, upperBound)
                    self.genes[i][offset + 1] = max(lowerBound, upperBound)

    @staticmethod
    def zero_or_one(value):
        """
        Used a finalization point to convert the floats to zeros or ones.
        :param value:
        :return:
        """
        if value < 0:
            return 0

        if value > 1:
            return 1
        else:
            return value

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def setGeneFromIndex(self, i, j, val):
        self.genes[i][j] = val

    def mutation_output(self, mutation_rate):
        """
        Mutate to 1 because we power it at the end.
        :param mutation_rate:
        :return:
        """
        for i in range(len(self.genes)):
            if mutation_rate > random():
                the_gene_in_question = self.genes[i][len(self.genes[i]) - 1]
                self.genes[i][len(self.genes[i]) - 1] = int(the_gene_in_question ^ 1)
