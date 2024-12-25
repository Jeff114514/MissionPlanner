from population import *

class GA:

    @classmethod
    def evolvePopulation(cls, pop):
        newPopulation = Population(pop.populationSize, False)
        elitismOffset = 0
        if elitism:
            newPopulation.saveRoute(0, pop.getFittest())
            elitismOffset = 1

        cumulative_fitness = []
        current_sum = 0
        index = list(range(pop.populationSize))
        random.shuffle(index)
        for i in range(pop.populationSize):
            current_sum += pop.getRoute(index[i]).getFitness()
            cumulative_fitness.append(current_sum)

        for i in range(elitismOffset, newPopulation.populationSize):
            parent1 = cls.rouletteWheelSelection(pop, index, cumulative_fitness)
            parent2 = cls.rouletteWheelSelection(pop, index, cumulative_fitness)
            child = cls.pmxCrossover(parent1, parent2)
            newPopulation.saveRoute(i, child)

        for i in range(elitismOffset, newPopulation.populationSize):
            cls.swapMutation(newPopulation.getRoute(i))

        return newPopulation

    @classmethod
    def pmxCrossover(cls, parent1, parent2):
        child = Route()
        child.base.append(Dustbin(-1, -1)) # since size is (numNodes - 1) by default
        startPos = 0
        endPos = 0
        startPos, endPos = random.sample(range(numNodes), 2)

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
        index1, index2 = random.sample(range(numTrucks), 2)
        #print ('Indexes selected: ' + str(index1) + ',' + str(index2))
        if route.routeLengths[index1] <= 2 or route.routeLengths[index2] <= 2 or random.randrange(1) < mutationRate:
            return
        #generate replacement range for 1
        route1startPos = 0
        route1lastPos = 0
        while route1startPos > route1lastPos or route1startPos == 1:
            route1startPos = random.randint(1, route.routeLengths[index1] - 1)
            route1lastPos = random.randint(1, route.routeLengths[index1] - 1)

        #generate replacement range for 2
        route2startPos = 0
        route2lastPos = 0
        while route2startPos > route2lastPos or route2startPos == 1:
            route2startPos = random.randint(1, route.routeLengths[index2] - 1)
            route2lastPos= random.randint(1, route.routeLengths[index2] - 1)
        # print ('startPos, lastPos: ' + str(route1startPos) + ',' + str(route1lastPos) + ',' + str(route2startPos) + ',' + str(route2lastPos))
        swap1 = [] # values from 1
        swap2 = [] # values from 2

        # pop all the values to be replaced
        for i in range(route1startPos, route1lastPos + 1):
            swap1.append(route.route[index1].pop(route1startPos))

        for i in range(route2startPos, route2lastPos + 1):
            swap2.append(route.route[index2].pop(route2startPos))

        del1 = (route1lastPos - route1startPos + 1)
        del2 = (route2lastPos - route2startPos + 1)

        # add to new location by pushing
        route.route[index1][route1startPos:route1startPos] = swap2
        route.route[index2][route2startPos:route2startPos] = swap1

        route.routeLengths[index1] = len(route.route[index1])
        route.routeLengths[index2] = len(route.route[index2])

    @classmethod
    def rouletteWheelSelection(cls, pop, index, cumulative_fitness):
        max_fitness = cumulative_fitness[-1]
        winners = Population(tournamentSize, False)
        for i in range(tournamentSize):
            pick = random.uniform(0, max_fitness)
            idx = cls.binarySearch(cumulative_fitness, pick)
            winners.saveRoute(i, pop.getRoute(index[idx]))
        return winners.getFittest()

    @classmethod
    def binarySearch(cls, cumulative_fitness, pick):
        low = 0
        high = len(cumulative_fitness) - 1
        while low < high:
            mid = (low + high) // 2
            if cumulative_fitness[mid] < pick:
                low = mid + 1
            else:
                high = mid
        return low
