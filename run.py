import os
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
from myACO import ACO

dict = { # 目标数，无人机数，迭代次数，种群大小
    '30_10': [30, 10, 400, 100],
    '200_20': [200, 20, 400, 120],
    '500_30': [500, 30, 400, 140]
}
seed = int(1735126954)

for key, value in dict.items():
    numNodes, numTrucks, numIterations, numPopulations = value
    # os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(numIterations)+" "+str(numPopulations)+" "+str(seed)+" GA")
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(numIterations)+" "+str(numPopulations)+" "+str(seed)+" myGA")
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(numIterations)+" "+str(numPopulations)+" "+str(seed)+" myPSO")


drawDict = {
    '30_10': [30, 10, 400, 100],
    '200_20': [200, 20, 400, 120],
    '500_30': [500, 30, 400, 140]
}
for key, value in drawDict.items():
    numNodes, numTrucks, numIterations, numPopulations = value
    df1 = pd.read_csv('GA'+str(numNodes)+'_'+str(numTrucks)+'_'+str(numIterations)+'_'+str(numPopulations)+'.csv')
    df2 = pd.read_csv('myGA'+str(numNodes)+'_'+str(numTrucks)+'_'+str(numIterations)+'_'+str(numPopulations)+'.csv')
    df3 = pd.read_csv('myPSO'+str(numNodes)+'_'+str(numTrucks)+'_'+str(numIterations)+'_'+str(numPopulations)+'.csv')

    xaxis = df1['xaxis']
    yaxis = df1['yaxis']

    xaxis2 = df2['xaxis']
    yaxis2 = df2['yaxis']

    xaxis3 = df3['xaxis']
    yaxis3 = df3['yaxis']

    # for i, y in enumerate(yaxis):
    #     if i == 0:
    #         yaxis[i] = y
    #     else:
    #         yaxis[i] = min(y, yaxis[i-1])

    # for i, y in enumerate(yaxis2):
    #     if i == 0:
    #         yaxis2[i] = y
    #     else:
    #         yaxis2[i] = min(y, yaxis2[i-1])
    # for i, y in enumerate(yaxis3):
    #     if i == 0:
    #         yaxis3[i] = y
    #     else:
    #         yaxis3[i] = min(y, yaxis3[i-1])

    #reset plt
    plt.clf()
    plt.title('numNodes: '+str(numNodes)+', numBots: '+str(numTrucks))

    plt.plot(xaxis, yaxis, 'r-', label='GA')
    plt.plot(xaxis2, yaxis2, 'b-', label='myGA')
    plt.plot(xaxis3, yaxis3, 'g-', label='myPSO')
    plt.legend()

    plt.savefig('result_'+str(numNodes)+'_'+str(numTrucks)+'.png')

    # df = pd.DataFrame({'GA': yaxis, 'myGA': yaxis2, 'myPSO': yaxis3, 'iteriation': range(max(len(yaxis), len(yaxis2), len(yaxis3)))})
    # df.to_csv('result_'+str(numNodes)+'_'+str(numTrucks)+'.csv', index=False)
