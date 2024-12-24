'''
The main helper class for Genetic Algorithm to perform
crossover, mutation on populations to evolve them
'''
from population import *

class GA:

    @classmethod
    # Evolve pop
    def evolvePopulation(cls, pop):

        newPopulation = Population(pop.populationSize, False)

        elitismOffset = 0
        # If fittest chromosome has to be passed directly to next generation
        if elitism:
            newPopulation.saveRoute(0, pop.getFittest())
            elitismOffset = 1

        # Performs tournament selection followed by crossover to generate child
        for i in range(elitismOffset, newPopulation.populationSize):
            parent1 = cls.rouletteWheelSelection(pop)
            parent2 = cls.rouletteWheelSelection(pop)
            child = cls.pmxCrossover(parent1, parent2)
            # Adds child to next generation
            newPopulation.saveRoute(i, child)


        # Performs Mutation
        for i in range(elitismOffset, newPopulation.populationSize):
            cls.swapMutation(newPopulation.getRoute(i))

        return newPopulation

    # Function to implement crossover operation
    @classmethod
    def pmxCrossover (cls, parent1, parent2):
        child = Route()
        child.base.append(Dustbin(-1, -1)) # since size is (numNodes - 1) by default
        startPos = 0
        endPos = 0
        while (startPos >= endPos):
            startPos = random.randint(1, numNodes-1)
            endPos = random.randint(1, numNodes-1)

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
            if not(child.containsDustbin(parent2.base[i])):
                for i1 in range(numNodes):
                    if child.base[i1].checkNull():
                        child.base[i1] =  parent2.base[i]
                        break

        k=0
        child.base.pop(0)
        for i in range(numTrucks):
            child.route[i].append(RouteManager.getDustbin(0)) # add same first node for each route
            for j in range(child.routeLengths[i]-1):
                child.route[i].append(child.base[k]) # add shuffled values for rest
                k+=1
        return child

    # Mutation opeeration
    @classmethod
    def swapMutation (cls, route):
        for i in range(numTrucks):
            if random.random() < mutationRate and route.routeLengths[i] > 2:
                swapIndex1 = random.randint(1, route.routeLengths[i] - 1)
                swapIndex2 = random.randint(1, route.routeLengths[i] - 1)
                route.route[i][swapIndex1], route.route[i][swapIndex2] = route.route[i][swapIndex2], route.route[i][swapIndex1]

    # Tournament Selection: choose a random set of chromosomes and find the fittest among them 
    @classmethod
    def rouletteWheelSelection (cls, pop):
        maxFitness = sum(route.getFitness() for route in pop.routes)
        pick = random.uniform(0, maxFitness)
        current = 0
        for route in pop.routes:
            current += route.getFitness()
            if current > pick:
                return route
