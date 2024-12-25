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
globals.numIterations = int(args[3])
globals.numPopulations = int(args[4])
globals.seedValue = int(args[5])
Fn = args[6]
# #由numNodes和numTrucks计算
# globals.numGenerations = int((math.log(globals.numNodes*globals.numTrucks, math.e)+2) * 11.4)
# globals.populationSize = int((math.log(globals.numNodes * globals.numTrucks, 2)+4) * 5.14 + globals.numTrucks)


if Fn == 'myGA':
    from myGA import *
elif Fn == 'GA':
    from galogic import *
elif Fn == 'myPSO':
    from myPSO import *
else:
    print('Invalid function name')
    exit()

# Add Dustbins
random.seed(seedValue)
globals.print_all()
for i in range(numNodes):
    RouteManager.addDustbin(Dustbin())
    globals.dustbins.append(RouteManager.getDustbin(i))

data = []
for i in range(len(globals.dustbins)):
    data.append([globals.dustbins[i].getX(), globals.dustbins[i].getY()])
data = pd.DataFrame({'x': [i[0] for i in data], 'y': [i[1] for i in data]})
data.to_csv('dustbins'+str(numNodes)+'.csv', index=False)


startPoint = (RouteManager.getDustbin(0).getX(), RouteManager.getDustbin(0).getY())
    

yaxis = [] # Fittest value (distance)
xaxis = [] # Generation count

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
basic_route = globalRoute.getRoute()
print ('Initial minimum distance: ' + str(globalRoute.getDistance()))

# Start evolving
cnt = 50
for i in pbar(range(numGenerations)):
    cnt -= 1
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
        cnt = 50
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)
    if cnt <= 0:
        print("stop at generation", i)
        break
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

plt.savefig(Fn+str(numNodes)+'_'+str(numTrucks)+'_'+str(numGenerations)+'_'+str(populationSize)+'.png')
# cnt = 0
# for i in range(numTrucks):
#     if len(basic_route[i]) > 0:
#         cnt += 1
#     plt.plot([dustbin.getX() for dustbin in basic_route[i]], [dustbin.getY() for dustbin in basic_route[i]], color=plt.cm.rainbow(cnt/numTrucks))
# #draw all dustbins
# for i in range(numNodes):
#     plt.scatter(globals.dustbins[i].getX(), globals.dustbins[i].getY(), color='blue')
# plt.show()
# plt.clf()

df = pd.DataFrame({'xaxis': xaxis, 'yaxis': yaxis, 'seed': localSeed})

df.to_csv(Fn+str(numNodes)+'_'+str(numTrucks)+'_'+str(numGenerations)+'_'+str(populationSize)+'.csv', index=False)
