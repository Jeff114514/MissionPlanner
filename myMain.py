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
globals.seedValue = int(args[3])
Fn = args[4]
#由numNodes和numTrucks计算
globals.tournamentSize = int(math.log(globals.numNodes * globals.numTrucks, 2) + globals.numTrucks)
globals.numGenerations = int((math.log(globals.numNodes*globals.numTrucks, math.e)+1) * 12)
globals.populationSize = int(math.log(globals.numNodes * globals.numTrucks, 2) * 20 - globals.numTrucks)


if Fn == 'myGA':
    from myGA import *
elif Fn == 'GA':
    from galogic import *
elif Fn == 'myPSO':
    from myACO import *
else:
    print('Invalid function name')
    exit()

# Add Dustbins
localSeed = seedValue * numNodes * numTrucks
random.seed(localSeed)
globals.print_all()
for i in range(numNodes):
    RouteManager.addDustbin(Dustbin())
    globals.dustbins.append(RouteManager.getDustbin(i))

yaxis = [] # Fittest value (distance)
xaxis = [] # Generation count

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
basic_route = globalRoute.getRoute()
print ('Initial minimum distance: ' + str(globalRoute.getDistance()))

# Start evolving
cnt = 0
for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)
final_route = globalRoute.getRoute()
print ('Global minimum distance: ' + str(globalRoute.getDistance()))
print ('Final Route: ' + globalRoute.toString())

#draw all routes in different colors for different trucks
cnt = 0
for i in range(numTrucks):
    if len(final_route[i]) > 0:
        cnt += 1
    plt.plot([dustbin.getX() for dustbin in final_route[i]], [dustbin.getY() for dustbin in final_route[i]], color=plt.cm.rainbow(cnt/numTrucks))
#draw all dustbins
for i in range(numNodes):
    plt.scatter(globals.dustbins[i].getX(), globals.dustbins[i].getY(), color='blue')
plt.show()
plt.clf()

cnt = 0
for i in range(numTrucks):
    if len(basic_route[i]) > 0:
        cnt += 1
    plt.plot([dustbin.getX() for dustbin in basic_route[i]], [dustbin.getY() for dustbin in basic_route[i]], color=plt.cm.rainbow(cnt/numTrucks))
#draw all dustbins
for i in range(numNodes):
    plt.scatter(globals.dustbins[i].getX(), globals.dustbins[i].getY(), color='blue')
plt.show()
plt.clf()

df = pd.DataFrame({'xaxis': xaxis, 'yaxis': yaxis, 'seed': localSeed})

if Fn == 'myGA':
    df.to_csv('myMain'+str(numNodes)+'_'+str(numTrucks)+'.csv', index=False)
else:
    df.to_csv('main'+str(numNodes)+'_'+str(numTrucks)+'.csv', index=False)
