import random
import math
import time
'''
Contains all global variables specific to simulation
'''
# Defines range for coordinates when dustbins are randomly scattered
xMax = 1000
yMax = 1000
seedValue = 1
numNodes = 30
numGenerations = 70
# size of population
populationSize = 100
mutationRate = 0.05
tournamentSize = 10
elitism = True
# number of trucks
numTrucks = 10
distanceMatrix = None
dustbinInitCnt = 0
dustbins = []

def random_range(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

# Randomly distribute number of dustbins to subroutes
# Maximum and minimum values are maintained to reach optimal result
def route_lengths():
    upper = (numNodes + numTrucks - 1)
    fa = upper/numTrucks*(1 + math.log(numTrucks)/2) # max route length 
    fb = upper/numTrucks/(1 + math.log(numTrucks)/2) # min route length
    a = random_range(numTrucks, upper)
    while 1:
        if all( i < fa and i > fb  for i in a):
            break
        else:
            # if max(a) > fa:
            #     fa+=0.05
            if min(a) < fb - 1e-3:
                fb-=0.05
            a = random_range(numTrucks, upper)
    # print(a)
    return a

def print_all():
    print(numNodes, numTrucks, numGenerations, populationSize, tournamentSize)

def timmer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} Time taken: {end - start} seconds")
        return result
    return wrapper

def initDistanceMatrix():
    Matrix = [[0 for _ in range(len(dustbins))] for _ in range(len(dustbins))]
    for i in range(len(dustbins)):
        for j in range(len(dustbins)):
            dx = dustbins[i].getX() - dustbins[j].getX()
            dy = dustbins[i].getY() - dustbins[j].getY()
            if dustbins[i].id != -1 or dustbins[j].id != -1:
                Matrix[i][j] = math.sqrt(dx*dx + dy*dy)
            else:
                Matrix[i][j] = math.inf
    return Matrix

