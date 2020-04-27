class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def getWeight(self):
        return self.weight

    def getValue(self):
        return self.value

class Knapsack:
    def __init__(self, capacity, items):
        self.currentSolution = [False]*len(items)
        self.neighbourSolutions = []
        self.capacity = capacity
        self.items = items
        self.iterationCount = 0

    def generateNeighbourSolutions(self):
        #Generate Hamming vectors as neighbourSolution and store them in neighbourSolutions
        self.neighbourSolutions = []
        n = len(self.currentSolution)
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
        for i in range(n):
            solutionWeight[i] = self.getWeight(self.neighbourSolutions[i])
            solutionValue[i] = self.getValue(self.neighbourSolutions[i])

        #Find the highest value from the neighbour solutions and replace current solution if higher
        bestValue = self.getValue(self.currentSolution)
        indexBestValue = -1
        for j in range(n):
            if solutionWeight[j]<=capacity and solutionValue[j]>bestValue:
                bestValue = solutionValue[j]
                indexBestValue = j
        if indexBestValue != -1:
            self.currentSolution = self.neighbourSolutions[indexBestValue]
            return True
        return False
    
    def printCurrentSolution(self):
        self.iterationCount += 1
        i = str(self.iterationCount)
        s = str(list(map(int, self.currentSolution)))
        v = str(self.getValue(self.currentSolution))
        w = str(self.getWeight(self.currentSolution))
        print('Iteration ' + i +': ' + s + ' Value: ' + v + ' Weight: ' + w)

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

    print('Capacity: ', capacity)
    print('Number of items: ', n)
    print('Weights: ', weights)
    print('Values: ', values)
    print()

    items = []
    for i in range(n):
        item = Item(weights[i], values[i])
        items.append(item)

    knapsack = Knapsack(capacity, items)

    while True:
        knapsack.generateNeighbourSolutions()
        if knapsack.findNextSolution():
            knapsack.printCurrentSolution()
        else:
            print()
            break
