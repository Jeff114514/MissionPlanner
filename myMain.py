import globals
import matplotlib.pyplot as plt
import progressbar
import sys
import pandas as pd
import math
pbar = progressbar.ProgressBar()

args = sys.argv
globals.numNodes = int(args[1])
globals.numTrucks = int(args[2])
Fn = args[3]
#由numNodes和numTrucks计算numGenerations
globals.numGenerations = int((math.log(globals.numNodes*globals.numTrucks, math.e)+1) * 10)
globals.populationSize = int(math.log(globals.numNodes * globals.numTrucks, 2) * 10)


if Fn == 'myGA':
    from myGA import *
else:
    from galogic import *

# Add Dustbins
random.seed(seedValue * numNodes * numTrucks * numGenerations * populationSize)
globals.print_all()
for i in range(numNodes):
    RouteManager.addDustbin(Dustbin())

yaxis = [] # Fittest value (distance)
xaxis = [] # Generation count

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
print ('Initial minimum distance: ' + str(globalRoute.getDistance()))

# Start evolving
for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)

print ('Global minimum distance: ' + str(globalRoute.getDistance()))
print ('Final Route: ' + globalRoute.toString())


df = pd.DataFrame({'xaxis': xaxis, 'yaxis': yaxis})

if Fn == 'myGA':
    df.to_csv('myMain'+str(numNodes)+'_'+str(numTrucks)+'.csv', index=False)
else:
    df.to_csv('main'+str(numNodes)+'_'+str(numTrucks)+'.csv', index=False)
