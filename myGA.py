from population import *

class GA:

    @classmethod
    def evolvePopulation(cls, pop):
        newPopulation = Population(pop.populationSize, False)
        elitismOffset = 0
        if elitism:
            newPopulation.saveRoute(0, pop.getFittest())
            elitismOffset = 1

        # 预先计算累积适应度
        cumulativeFitness = cls.precomputeCumulativeFitness(pop)

        for i in range(elitismOffset, newPopulation.populationSize):
            parent1 = cls.rouletteWheelSelection(pop, cumulativeFitness)
            parent2 = cls.rouletteWheelSelection(pop, cumulativeFitness)
            child = cls.pmxCrossover(parent1, parent2)
            newPopulation.saveRoute(i, child)

        for i in range(elitismOffset, newPopulation.populationSize):
            cls.swapMutation(newPopulation.getRoute(i))

        return newPopulation

    @classmethod
    def pmxCrossover(cls, parent1, parent2):
        child = Route()
        child.base.append(Dustbin(-1, -1))
        startPos = random.randint(1, numNodes - 1)
        endPos = random.randint(1, numNodes - 1)

        if startPos > endPos:
            startPos, endPos = endPos, startPos

        parent1.base = [parent1.route[0][0]]
        parent2.base = [parent2.route[0][0]]

        for i in range(numTrucks):
            for j in range(1, parent1.routeLengths[i]):
                parent1.base.append(parent1.route[i][j])


        for i in range(numTrucks):
            for j in range(1, parent2.routeLengths[i]):
                parent2.base.append(parent2.route[i][j])

        for i in range(1, numNodes):
            if i > startPos and i < endPos:
                child.base[i] = parent1.base[i]

        for i in range(numNodes):
            if not child.containsDustbin(parent2.base[i]):
                for j in range(numNodes):
                    if child.base[j].checkNull():
                        child.base[j] = parent2.base[i]
                        break

        k = 0
        child.base.pop(0)
        for i in range(numTrucks):
            child.route[i].append(RouteManager.getDustbin(0))
            for j in range(child.routeLengths[i] - 1):
                child.route[i].append(child.base[k])
                k += 1
        return child

    @classmethod
    def swapMutation(cls, route):
        for i in range(numTrucks):
            if random.random() < mutationRate and route.routeLengths[i] > 2:
                swapIndex1 = random.randint(1, route.routeLengths[i] - 1)
                swapIndex2 = random.randint(1, route.routeLengths[i] - 1)
                route.route[i][swapIndex1], route.route[i][swapIndex2] = route.route[i][swapIndex2], route.route[i][swapIndex1]

    @classmethod
    def precomputeCumulativeFitness(cls, pop):
        cumulativeFitness = []
        currentSum = 0
        for route in pop.routes:
            currentSum += route.getFitness()
            cumulativeFitness.append(currentSum)
        return cumulativeFitness

    @classmethod
    def rouletteWheelSelection(cls, pop, cumulativeFitness):
        maxFitness = cumulativeFitness[-1]
        pick = random.uniform(0, maxFitness)
        index = cls.binarySearch(cumulativeFitness, pick)
        return pop.routes[index]

    @staticmethod
    def binarySearch(cumulativeFitness, pick):
        low, high = 0, len(cumulativeFitness) - 1
        while low < high:
            mid = (low + high) // 2
            if cumulativeFitness[mid] < pick:
                low = mid + 1
            else:
                high = mid
        return low