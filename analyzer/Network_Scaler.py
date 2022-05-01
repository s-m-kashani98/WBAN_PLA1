import os,random,AIModel,csv

from numpy.core.fromnumeric import repeat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

iniFile = "/home/moh/Documents/PhD/research/Castalia/Simulations/BANtest/omnetpp.ini"
Castalia_BAN_Test_Path = "/home/moh/Documents/PhD/research/Castalia/Simulations/BANtest"
numNodes = 8
Hub = 6
attacker =7
goodRange = (0,1.5)
badRange = (12,14)
hubRange = (12.5,13.5)

def rand(arr,strt,end):
    temp  = round(random.random()*(end-strt)+strt,1)
    while temp in arr:
        temp  = round(random.random()*(end-strt)+strt,1)
    return temp
    
def nodePlacement(good,bad,hub):
    #0 is R-ankle
    #1 is L-ankle
    #2 is R-wrist
    #3 is L-wrist
    #4 is R-hip 
    #5 is chest

    ### standing
    xCoor = [13.05,  13.40,   13.0,  13.30,  13.03, 13.30,  0,  0]
    yCoor = [13.05,  13.05,   13.05,  13.05,  13.05,  13.05,  0,  0]
    zCoor = [0.1,   .1,   1.00,  1.00,  1.1,  1.5,  0,  0]

    

    xCoor[Hub] = rand(xCoor,hub[0],hub[1]) + .6*((-1)**random.randint(0,1))
    yCoor[Hub] = rand(yCoor,hub[0],hub[1]) + .6*((-1)**random.randint(0,1))
    zCoor[Hub] = rand(zCoor,0,2)

    xCoor[attacker] = rand(xCoor,bad[0],bad[1]) + 5.6*((-1)**random.randint(0,1))
    yCoor[attacker] = rand(yCoor,bad[0],bad[1]) + 5.6*((-1)**random.randint(0,1))
    zCoor[attacker] = rand(zCoor,0,2)
    #print(xCoor,"\n",yCoor,"\n",zCoor,"\n")
    return xCoor,yCoor,zCoor

def run(Coor):
    xCoor,yCoor,zCoor = Coor
    f = open(iniFile, "w+")

    x= """[General]
include ../Parameters/Castalia.ini
sim-time-limit = 50000s  # 

SN.numNodes = 8
#SN.field_x =  100
#SN.field_y =  100
#SN.field_z  = 5

SN.wirelessChannel.onlyStaticNodes = true
#SN.wirelessChannel.pathLossMapFile = "../Parameters/WirelessChannel/BANmodels/pathLossMap.txt"
SN.wirelessChannel.temporalModelParametersFile = "../Parameters/WirelessChannel/BANmodels/TemporalModel.txt"
SN.wirelessChannel.xCellSize = 0.01
SN.wirelessChannel.yCellSize = 0.01
SN.wirelessChannel.zCellSize = 0.01
SN.wirelessChannel.collectTraceInfo = false


SN.node[*].Communication.Radio.RadioParametersFile = "../Parameters/Radio/BANRadio.txt"
SN.node[*].Communication.Radio.symbolsForRSSI = 16
SN.node[0].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[1].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[2].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[3].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[4].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[5].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[6].Communication.Radio.TxOutputPower = "-20dBm"
SN.node[7].Communication.Radio.TxOutputPower = "-20dBm" """ + "\nSN.node[0].xCoor = "+str(
round(xCoor[0],2))+"\nSN.node[1].xCoor = "+str(
round(xCoor[1],2))+"\nSN.node[2].xCoor = "+str(
round(xCoor[2],2))+"\nSN.node[3].xCoor = "+str(
round(xCoor[3],2))+"\nSN.node[4].xCoor = "+str(
round(xCoor[4],2))+"\nSN.node[5].xCoor = "+str(
round(xCoor[5],2))+"\nSN.node[6].xCoor = "+str(
round(xCoor[6],2))+"\nSN.node[7].xCoor = "+str(
round(xCoor[7],2))+"\nSN.node[0].yCoor = "+str(
round(yCoor[0],2))+"\nSN.node[1].yCoor = "+str(
round(yCoor[1],2))+"\nSN.node[2].yCoor = "+str(
round(yCoor[2],2))+"\nSN.node[3].yCoor = "+str(
round(yCoor[3],2))+"\nSN.node[4].yCoor = "+str(
round(yCoor[4],2))+"\nSN.node[5].yCoor = "+str(
round(yCoor[5],2))+"\nSN.node[6].yCoor = "+str(
round(yCoor[6],2))+"\nSN.node[7].yCoor = "+str(
round(yCoor[7],2))+"\nSN.node[0].zCoor = "+str(
round(zCoor[0],2))+"\nSN.node[1].zCoor = "+str(
round(zCoor[1],2))+"\nSN.node[2].zCoor = "+str(
round(zCoor[2],2))+"\nSN.node[3].zCoor = "+str(
round(zCoor[3],2))+"\nSN.node[4].zCoor = "+str(
round(zCoor[4],2))+"\nSN.node[5].zCoor = "+str(
round(zCoor[5],2))+"\nSN.node[6].zCoor = "+str(
round(zCoor[6],2))+"\nSN.node[7].zCoor = "+str(
round(zCoor[7],2))+"""
#SN.node[*].Communication.Radio.collectTraceInfo = true
SN.node[*].Communication.MAC.collectTraceInfo = true
#SN.node[*].Application.collectTraceInfo = true

SN.node[*].ResourceManager.baselineNodePower = 0
SN.node[*].Communication.MACProtocolName = "BaselineBANMac"
SN.node[*].Communication.MAC.phyDataRate = 1024
SN.node[6].Communication.MAC.isHub = true
SN.node[*].Communication.MAC.macBufferSize = 48
SN.node[*].ApplicationName = "ThroughputTest"
SN.node[*].Application.startupDelay = 1  	#wait for 1sec before starting sending packets
SN.node[6].Application.latencyHistogramMax = 600
SN.node[6].Application.latencyHistogramBuckets = 30
SN.node[0].Application.packet_rate = 3
SN.node[1].Application.packet_rate = 3
SN.node[2].Application.packet_rate = 3
SN.node[3].Application.packet_rate = 3
SN.node[4].Application.packet_rate = 1
SN.node[5].Application.packet_rate = 1
SN.node[6].Application.packet_rate = 0
SN.node[7].Application.packet_rate = 1"""

    #0 is R-ankle
    #1 is L-wrist
    #2 is R-wrist
    #3 is L-ankle
    #4 is R-hip 
    #5 is chest
    f.write(x)
    f.close()

    os.system("cd " + Castalia_BAN_Test_Path + """; rm 2*;
    rm Castalia-Trace.txt;../../bin/Castalia -c General;echo >>Castalia-Trace.txt; echo "";echo \"endendend\">> Castalia-Trace.txt""")














header = ["accuracy", "F1_Score", "FPR" ,"AUC"]
dataSet = open("img/dataSet.csv","w")
csvWriter = csv.writer(dataSet)
csvWriter.writerow(header)
repeat = 10
for i in range(repeat):
    print(str(i+1)+ " out of "+ str(repeat)+":")
    coor = nodePlacement(good =goodRange,bad = badRange,hub=hubRange)
    run(coor)
    os.system("cd /home/moh/Documents/PhD/research/analyzer; rm dataSet.csv;python3 analyzer.py;")
    
    
    
    plt.subplot(1,2,1)


    #Predictors = ["RSSI_AVG","RSSI_MIN","RSSI_MAX","RSSI_range","RSSI_STD"]#,"blckRate"]
    Predictors = ["RSSI_AVG","RSSI_MIN","RSSI_MAX","RSSI_range","RSSI_STD","blckRate"]

    acu, f_score,auc,FPR,confMat,clf= AIModel.AITrain(Predictors)


    print(coor)
    confMat = confMat.transpose()
    for i in range(numNodes):
        if i == Hub:
            plt.plot(coor[0][i], coor[2][i], 'o', color='blue')
        elif i != numNodes-1:
            plt.plot(coor[0][i], coor[2][i], 'o', color='black')
            plt.text(coor[0][i], coor[2][i], str(i))
        else:
            plt.plot(coor[0][i], coor[2][i], 'o', color='red')
    plt.title("accuracy: "+str(round(acu,3))+" - F_Score: "+ str(round(f_score,3))+ " - FPR: "+ str(round(FPR,3)) + " - AUC: "+ str(round(auc,3)))
    plt.subplot(1,2,2)
    
    for i in range(len(confMat)):
        for j in range(len(confMat[0])):
            x = confMat[i][j]
            plt.text(i,(j+1)%2,str(x))
    plt.plot(-.5,-.5)
    plt.plot(1.5,1.5)
            

    plt.savefig("/home/moh/Documents/PhD/research/analyzer/img/F_Score:"+ str(round(f_score,3))+ ":FPR:"+ str(round(FPR,3))+":.jpg")
    plt.close()


    csvWriter.writerow([round(acu,3),round(f_score,3),round(FPR,3),round(auc,3),confMat[0][0],confMat[0][1],confMat[1][0],confMat[1][1]])
dataSet.close()
     