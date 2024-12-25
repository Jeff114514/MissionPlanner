import os
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
from myACO import ACO
'''
1、	在30个任务点和10架无人机的情况下得到收敛解并可视化出来。
2、	在200个任务点和20架无人机的情况下得到收敛解并可视化出来。
3、	在500个任务点和30架无人机的情况下得到收敛解并可视化出来。
'''
dict = { # 目标数，无人机数，迭代次数，种群大小
    '30_10': [30, 10, 70, 100],
    '200_20': [200, 20, 70, 100],
    '500_30': [500, 30, 70, 100]
}
seed = int(time.time())

for key, value in dict.items():
    numNodes, numTrucks, numIterations, numPopulations = value
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(numIterations)+" "+str(numPopulations)+" "+str(seed)+" GA")
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(numIterations)+" "+str(numPopulations)+" "+str(seed)+" myGA")
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(numIterations)+" "+str(numPopulations)+" "+str(seed)+" myPSO")



for key, value in dict.items():
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

    #reset plt
    plt.clf()
    plt.title('GA-r, myGA-b, myPSO-g')

    plt.plot(xaxis, yaxis, 'r-', label='GA')
    plt.plot(xaxis2, yaxis2, 'b-', label='myGA')
    plt.plot(xaxis3, yaxis3, 'g-', label='myPSO')

    plt.savefig('result_'+str(numNodes)+'_'+str(numTrucks)+'.png')
