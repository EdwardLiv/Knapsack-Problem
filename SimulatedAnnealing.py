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
    def __init__(self, capacity, items, initialTemperature, finalTemperature, updateTemperature):
        self.currentSolution = [False]*len(items)
        self.bestFoundSolution = [False]*len(items)
        self.neighbourSolutions = []
        self.currentTemperature = initialTemperature
        self.finalTemperature = finalTemperature
        self.updateTemperature = updateTemperature
        self.capacity = capacity
        self.items = items
        self.iterationCount = 0

    def generateNeighbourSolutions(self):
        #Generate Hamming vectors as neighbourSolution and store them in neighbourSolutions
        n = len(self.currentSolution)
        self.neighbourSolutions = []
        for j in range(n):
            neighbourSolution = []
            for i in range(n):
                if i==j:
                    neighbourSolution.append(not self.currentSolution[i])
                else:
                    neighbourSolution.append(self.currentSolution[i])
            self.neighbourSolutions.append(neighbourSolution)

    def findNextSolution(self):
        #Find the weights and values of the neighbour solutions and store them in solutionWeight and solutionValue
        n = len(self.neighbourSolutions)
        solutionWeight = [0]*n
        solutionValue = [0]*n
        for j in range(n):
            for i in range(n):
                if self.neighbourSolutions[j][i]:
                    solutionWeight[j] += self.items[i].getWeight()
                    solutionValue[j] += self.items[i].getValue()

        #Find the highest value from random neighbour solutions
        neighbourMaxValue = self.getValue(self.currentSolution)
        indexNeighbourMaxValue = -1
        for attempt in range(n):
            i = np.random.randint(n)
            currentSolutionValue = self.getValue(self.currentSolution)
            probability = np.exp(-np.absolute(currentSolutionValue-solutionValue[i])/self.currentTemperature)
            #print('Probability:', probability*100, 'Temperature:', self.currentTemperature)

            if solutionWeight[i] <= capacity and (solutionValue[i] > neighbourMaxValue or probability > np.random.random()):
                neighbourMaxValue = solutionValue[i]
                indexNeighbourMaxValue = i

        #Lower temperature
        if self.currentTemperature > self.finalTemperature:
            self.currentTemperature -= self.updateTemperature
        else:
            self.currentTemperature = self.finalTemperature

        #Replace current solution if the neighbour solution has higher value
        if indexNeighbourMaxValue != -1:
            self.currentSolution = self.neighbourSolutions[indexNeighbourMaxValue]

            #Replace best found solution if the new current solution has higher value
            neighbourMaxValue = self.getValue(self.neighbourSolutions[indexNeighbourMaxValue])
            bestFoundSolutionMaxValue = self.getValue(self.bestFoundSolution)
            if neighbourMaxValue > bestFoundSolutionMaxValue:
                self.bestFoundSolution = self.neighbourSolutions[indexNeighbourMaxValue]
    
    def printCurrentSolution(self):
        self.iterationCount += 1
        i = str(self.iterationCount)
        s = str(list(map(int, self.currentSolution)))
        v = str(self.getValue(self.currentSolution))
        w = str(self.getWeight(self.currentSolution))
        print('Iteration ' + i +': ' + s + ' Value: ' + v + ' Weight: ' + w)

    def printBestFoundSolution(self):
        s = str(list(map(int, self.bestFoundSolution)))
        v = str(self.getValue(self.bestFoundSolution))
        w = str(self.getWeight(self.bestFoundSolution))
        print('\nBest solution found: ' + s + ' Value: ' + v + ' Weight: ' + w + '\n')

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
    #Optimal solution is 1458 value [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]

    initialTemperature = 200
    finalTemperature = 40
    updateTemperature = 0.2

    print('Capacity:', capacity)
    print('Number of items:', n)
    print('Weights:', weights)
    print('Values:', values)
    print()

    print('Initial temperature:', initialTemperature)
    print('Update temperature each step by:', updateTemperature)
    print()

    iterations = int(input('Insert number of iterations: '))
    print()

    items = []
    for i in range(n):
        item = Item(weights[i], values[i])
        items.append(item)

    knapsack = Knapsack(capacity, items, initialTemperature, finalTemperature, updateTemperature)

    for i in range(iterations):
        knapsack.generateNeighbourSolutions()
        knapsack.findNextSolution()
        knapsack.printCurrentSolution()

    knapsack.printBestFoundSolution()
