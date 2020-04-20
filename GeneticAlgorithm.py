import numpy as np

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def getWeight(self):
        return self.weight

    def getValue(self):
        return self.value

class Knapsack:
    def __init__(self, capacity, items, populationSize, mutationRate):
        self.population = [[False]*len(items) for i in range(populationSize)]
        self.wheelOfFortune = []
        self.mutationRate = mutationRate
        self.bestPhenotype = []
        self.capacity = capacity
        self.items = items
        self.generationCount = 0

    def initializePopulation(self):
        populationSize = len(self.population)
        phenotypeSize = len(items)

        #Get the weight list of all items
        itemWeight = [0]*phenotypeSize
        for i in range(phenotypeSize):
            itemWeight[i] = self.items[i].getWeight()

        for phenotype in range(populationSize):
            #Select genotypes in random order
            genotypeRandomOrder = list(range(0, phenotypeSize))
            np.random.shuffle(genotypeRandomOrder)

            #Chance to modify genotype while weight is less than capacity
            phenotypeWeight = 0
            for genotype in genotypeRandomOrder:
                potentialGenotypeWeight = itemWeight[genotype]
                if np.random.random() > 0.5 and self.capacity >= phenotypeWeight+potentialGenotypeWeight:
                    self.population[phenotype][genotype] = True
                    phenotypeWeight += potentialGenotypeWeight

    def selectPopulation(self):
        #Evaluate fitness of all population
        populationSize = len(self.population)
        fitness = [0]*populationSize
        totalFitness = 0
        for phenotype in range(populationSize):
            weight = self.getWeight(self.population[phenotype])
            if weight > capacity:
                fitness[phenotype] = 0
            else:
                fitness[phenotype] = self.getValue(self.population[phenotype])
                totalFitness += fitness[phenotype]

        #Fill wheel of fortune
        self.wheelOfFortune = []
        for phenotype in range(populationSize):
            n = int(fitness[phenotype]/totalFitness*100)
            for i in range(n):
                self.wheelOfFortune.append(self.population[phenotype])

    def evolvePopulation(self):
        wheelOfFortuneSize = len(self.wheelOfFortune)
        populationSize = len(self.population)

        #Delete previous generation
        self.population = []

        for i in range(populationSize):
            #Select random parents from wheel of fortune
            firstParent = self.wheelOfFortune[np.random.randint(wheelOfFortuneSize)]
            secondParent = self.wheelOfFortune[np.random.randint(wheelOfFortuneSize)]
            child = []
            phenotype = len(firstParent)
            for genotype in range(phenotype):

                #Crossover
                if np.random.random() > 0.5:
                    child.append(firstParent[genotype])
                else:
                    child.append(secondParent[genotype])

                #Chance to mutate
                if np.random.random() < self.mutationRate:
                    child[genotype] = not child[genotype]

            #Add child to new generation
            self.population.append(child)

    def printBestPhenotypeInGeneration(self):
        self.generationCount += 1
        populationSize = len(self.population)
        maxValue = 0
        indexMaxValue = 0

        for phenotype in range(populationSize):
            #Ignore if weight is greater than capacity
            weight = self.getWeight(self.population[phenotype])
            if weight < self.capacity:
                value = self.getValue(self.population[phenotype])

                #Replace best phenotype of current generation if higher
                if value > maxValue:
                    maxValue = value
                    indexMaxValue = phenotype

                    #Replace best phenotype of all generations if higher
                    if value > self.getValue(self.bestPhenotype):
                        self.bestPhenotype = self.population[phenotype]

        #Print
        g = str(self.generationCount)
        s = str(list(map(int, self.population[indexMaxValue])))
        v = str(self.getValue(self.population[indexMaxValue]))
        w = str(self.getWeight(self.population[indexMaxValue]))
        print('Best of generation ' + g +': ' + s + ' Value: ' + v + ' Weight: ' + w)

    def printBestPhenotype(self):
        s = str(list(map(int, self.bestPhenotype)))
        v = str(self.getValue(self.bestPhenotype))
        w = str(self.getWeight(self.bestPhenotype))
        print('\nBest phenotype found: ' + s + ' Value: ' + v + ' Weight: ' + w + '\n')

    def getWeight(self, solution):
        n = len(solution)
        solutionWeight = 0
        for i in range(n):
            if solution[i]:
                solutionWeight += self.items[i].getWeight()
        return solutionWeight

    def getValue(self, solution):
        n = len(solution)
        solutionValue = 0
        for i in range(n):
            if solution[i]:
                solutionValue += self.items[i].getValue()
        return solutionValue

if __name__ == "__main__":
    capacity = 750
    n = 15
    weights = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
    values = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]
    #Optimal solution is [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]

    populationSize = 100
    mutationRate = 0.05

    print('Capacity: ', capacity)
    print('Number of items: ', n)
    print('Weights: ', weights)
    print('Values: ', values)
    print()
    
    print('Population size of a generation:', populationSize)
    print('Mutation rate: ' + str(mutationRate*100) +'%')
    print()

    generationCount = int(input('Insert number of generations: '))
    print()

    items = []
    for i in range(n):
        item = Item(weights[i], values[i])
        items.append(item)

    knapsack = Knapsack(capacity, items, populationSize, mutationRate)
    knapsack.initializePopulation()

    for i in range(generationCount):
        knapsack.selectPopulation()
        knapsack.evolvePopulation()
        knapsack.printBestPhenotypeInGeneration()

    knapsack.printBestPhenotype()
