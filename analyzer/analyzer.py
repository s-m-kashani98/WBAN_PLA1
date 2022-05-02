import csv,os
from os import error

from numpy.core.fromnumeric import std


working_Path = os.getcwd().split('/')
del(working_Path[-1])
working_Path = '/'.join(working_Path)
# working_Path = "/home/moh/Documents/PhD/research/WBAN_PLA1"

Castalia_BAN_Test_Path = working_Path + "/Castalia/Simulations/BANtest"


header = ["RSSI_AVG","RSSI_MIN","RSSI_MAX","RSSI_range","RSSI_STD","blckRate","pcktTime","badNode","Node"]

Hub = 6


dataSet = open("dataSet.csv","w")
csvWriter = csv.writer(dataSet)
csvWriter.writerow(header)

f = open(Castalia_BAN_Test_Path+"/Castalia-Trace.txt", "r")


time = 0
numberOfNodes = 8
rssi = [[[]for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
blckRate = [[[]for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
blockTime = [[]for _ in range(numberOfNodes)]
blockTimeFlag = [True for _ in range(numberOfNodes)]
# recievedAt = [[0 for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
# rttTemp = [[-1 for _ in range(numberOfNodes)] for  _ in range(numberOfNodes)]
# rtt =  [[[]for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]



x = [""]
while "endendend" not in x[0]:
    x = f.readline().split(':')
    try:
        time = float(x[0].split("SN")[0])
    except:
        continue
    if "endendend" in x[0]:
        a=1
    
    
    if "A Packet recieved from src" in x[0] and int(x[7]) == Hub and int(x[11]) == 1 and int(x[1]) != 0 and int(x[5]) > 0: # x[7] is recieved at x[11] is isForMe bool
        if int(x[13]) > 2:
            rssi[int(x[1])][int(x[7])].append(float(x[9]))
        # if int(x[13]) == 4 not : #if ACK policy is BACK
        #     blockTimeFlag[int(x[1])] = True
            
    
    elif "transmitting B_ACK with src" in x[0]  and blockTimeFlag[int(x[3])] and int(x[11]) != 0: #if ACK policy is BACK:
        blckRate[int(x[1])][int(x[3])].append((int(x[9]),int(x[11])))
        blockTime[int(x[3])].append(time)
        blockTimeFlag[int(x[3])] = False
        if len(blockTime[int(x[3])]) > 1:
            tempBlockTime = time - blockTime[int(x[3])][-2]
        
            rssi_temp = rssi[int(x[3])][int(x[1])][-int(x[9]):len(rssi[int(x[3])][int(x[1])])]
            if len(rssi_temp) != 0:
                rssiAvgTemp = sum(rssi_temp)/len(rssi_temp)
            else:
                rssiAvgTemp = -300

            blckRateTemp = blckRate[int(x[1])][int(x[3])][-1][0]/blckRate[int(x[1])][int(x[3])][-1][1]
            if  int(x[3]) == 7:
                csvWriter.writerow([rssiAvgTemp,min(rssi_temp),max(rssi_temp),max(rssi_temp)-min(rssi_temp),std(rssi_temp), blckRateTemp, tempBlockTime,1, int(x[3])])
            else:
                csvWriter.writerow([rssiAvgTemp,min(rssi_temp),max(rssi_temp),max(rssi_temp)-min(rssi_temp),std(rssi_temp),blckRateTemp, tempBlockTime,0, int(x[3])])
           
    if "Sent from src" in x[0]:
        if int(x[7]) == 3:
            blockTimeFlag[int(x[1])] = True

f.close()       
dataSet.close()





























#     if "Packet recieved from src" in x[0] and not(int(x[1]) == 0 or int(x[7])==0):
#         rssi[int(x[1])][int(x[7])].append(float(x[9]))
#         recievedAt[int(x[1])][int(x[7])] +=  1
#         if rttTemp[int(x[7])][int(x[1])] != -1 and int(x[11]) == 1:
#             if rttTemp[int(x[3])][int(x[1])][1] == int(x[5]):
#                 rtt[int(x[1])][int(x[3])].append(time - rttTemp[int(x[3])][int(x[1])][0])
#                 rttTemp[int(x[1])][int(x[3])]=  -1
#     elif "Sent from src" in x[0]:
#         if (int(x[7]) == 4): #BACK - IACK 
#             rttTemp[int(x[1])][int(x[3])] = (time,int(x[5]))
#             blockTime[int(x[1])].append(time)
#             if blockTimeFlag[int(x[1])][1] == False:
#                 blockTimeFlag[int(x[1])] = (False,True)
#             else:
#                 blockTimeFlag[int(x[1])] = (True,True)



    
#     elif "transmitting B_ACK with src" in x[0]:
#         if blockTimeFlag[int(x[3])][0]:
#             blockTimeFlag[int(x[3])] = (False,True)
#             blockTime[int(x[3])][-1] -= time
#             if int(x[9]) != 0:
#                 myBlckTime = -blockTime[int(x[3])][-1]/int(x[9])
#         else:
#             # myBlckTime = blockTime[int(x[3])][-1]*10 
#             myBlckTime =  0
#         if int(x[9])>int(x[11]):
#             x[9] = "-1"
#         blckRate[int(x[1])][int(x[3])].append((int(x[9]),int(x[11])))
#         rssi_temp = rssi[int(x[3])][int(x[1])][-int(x[9]):len(rssi[int(x[3])][int(x[1])])]
#         if len(rssi_temp) != 0:
#             rssiAvgTemp = sum(rssi_temp)/len(rssi_temp)
#         else:
#             rssiAvgTemp = -300

#         blckRateTemp = 1        
#         if int(x[11]) != 0:
#             blckRateTemp = 80*float(x[9])/float(x[11])
#         if myBlckTime !=  0 or (rssiAvgTemp != min(rssi_temp))  or (min(rssi_temp)!= max(rssi_temp)):
#             if  int(x[3]) == 7:
#                 csvWriter.writerow([rssiAvgTemp,min(rssi_temp),max(rssi_temp),blckRateTemp,myBlckTime,1, int(x[3])])
#             else:
#                 csvWriter.writerow([rssiAvgTemp,min(rssi_temp),max(rssi_temp),blckRateTemp,myBlckTime,0, int(x[3])])

#     elif "BACK recieved" in x[0]:
#         rtt[int(x[1])][int(x[3])].append(time - rttTemp[int(x[3])][int(x[1])][0])
#         rttTemp[int(x[1])][int(x[3])]=  -1
        

# f.close()       
    




                


    
# rssiAVG = [[0 for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
# for i in range(len(rssi)):
#     for j in range(len(rssi[i])):
#         if len(rssi[i][j])!=0:
#             rssiAVG[i][j]= round(sum(rssi[i][j])/len(rssi[i][j]),1)

# rttAVG = [[0 for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
# for i in range(len(rtt)):
#     for j in range(len(rtt[i])):
#         if len(rtt[i][j])!=0:
#             rttAVG[i][j]= round(sum(rtt[i][j])/len(rtt[i][j]),8)
# rttAVG = rttAVG[6]
# del(rttAVG[0])


    
# blckRateAVG = [[0 for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
# for i in range(len(blckRate)):
#     for j in range(len(blckRate[i])):
#         if len(blckRate[i][j])!=0:
#             sumBlck = 0
#             for k in blckRate[i][j]:
#                 if k[1] != 0:
#                     sumBlck+= k[0]/k[1]
#             blckRateAVG[i][j]= round(sumBlck/len(blckRate[i][j]),4)
# print(blckRateAVG)
# blckRateAVG = blckRateAVG[6]
# del(blckRateAVG[0])


# del(recievedAt[0])
# for i in recievedAt:
#     del(i[0])

# del(rssiAVG[0])
# for i in rssiAVG:
#     del(i[0])


# rttMinMax = [[0 for _ in range(numberOfNodes)]for _ in range(numberOfNodes)]
# for i in range(len(rtt)):
#     for j in range(len(rtt[i])):
#         if len(rtt[i][j])!=0:
#             rttMinMax[i][j]= (round(min(rtt[i][j]),8),round(max(rtt[i][j]),8))
# rttMinMax = rttMinMax[6]
# del(rttMinMax[0])

# print("Block rate measured by the hub (avg)\n",blckRateAVG)
# print("rtt to Hub measured by Node (avg)\n",rttAVG)
# print("rtt (min,max)\n",rttMinMax)
# print("rssi of node i sensed at other nodes (avg)\n",rssiAVG)
# print("#packet from node i recieved at other nodes\n",recievedAt)



# dataSet.close()

