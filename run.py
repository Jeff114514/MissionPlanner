import os
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
'''
1、	在30个任务点和10架无人机的情况下得到收敛解并可视化出来。
2、	在200个任务点和20架无人机的情况下得到收敛解并可视化出来。
3、	在500个任务点和30架无人机的情况下得到收敛解并可视化出来。
'''
dict = {
    '30_10': [30, 10],
    '200_20': [200, 20],
    '500_30': [500, 30]
}
seed = int(time.time())

for key, value in dict.items():
    numNodes, numTrucks = value
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(seed)+" GA")
    os.system("python myMain.py "+str(numNodes)+" "+str(numTrucks)+" "+str(seed)+" myGA")

for key, value in dict.items():
    numNodes, numTrucks = value
    df1 = pd.read_csv('main'+str(numNodes)+'_'+str(numTrucks)+'.csv')
    df2 = pd.read_csv('myMain'+str(numNodes)+'_'+str(numTrucks)+'.csv')

    xaxis = df1['xaxis']
    yaxis = df1['yaxis']

    xaxis2 = df2['xaxis']
    yaxis2 = df2['yaxis']

    #reset plt
    plt.clf()

    plt.plot(xaxis, yaxis, 'r-', label='GA')
    plt.plot(xaxis2, yaxis2, 'b-', label='myGA')

    plt.savefig('result_'+str(numNodes)+'_'+str(numTrucks)+'.png')
