from population import *

class GA:

    @classmethod
    def evolvePopulation(cls, pop):
        newPopulation = Population(pop.populationSize, False)
        elitismOffset = 0
        if elitism:
            newPopulation.saveRoute(0, pop.getFittest())
            elitismOffset = 1

        for i in range(elitismOffset, newPopulation.populationSize):
            parent1 = cls.rouletteWheelSelection(pop)
            parent2 = cls.rouletteWheelSelection(pop)
            child = cls.pmxCrossover(parent1, parent2)
            newPopulation.saveRoute(i, child)

        for i in range(elitismOffset, newPopulation.populationSize):
            cls.swapMutation(newPopulation.getRoute(i))

        return newPopulation

    @classmethod
    def pmxCrossover(cls, parent1, parent2):
        child = Route()
        startPos = random.randint(1, numNodes - 1)
        endPos = random.randint(1, numNodes - 1)

        if startPos > endPos:
            startPos, endPos = endPos, startPos

        for i in range(startPos, endPos):
            child.base[i] = parent1.base[i]

        for i in range(numNodes):
            if i < len(parent2.base) and not child.containsDustbin(parent2.base[i]):
                for j in range(numNodes):
                    if child.base[j].checkNull():
                        child.base[j] = parent2.base[i]
                        break

        k = 0
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
    def rouletteWheelSelection(cls, pop):
        maxFitness = sum(route.getFitness() for route in pop.routes)
        pick = random.uniform(0, maxFitness)
        current = 0
        for route in pop.routes:
            current += route.getFitness()
            if current > pick:
                return route