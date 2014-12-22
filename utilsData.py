__author__ = 'jiusi'

import json
import numpy as np
import ntpath
import json

# status: Walking, Sitting, Running, Riding, Driving
# STAT_CODE = {'Walking':0, 'Sitting':1, 'Running':2, 'Riding':3, 'Driving':4}
STAT_CODE = {'Sitting':0, 'Driving':1, 'Riding':2, 'Walking':3, 'Running': 4}

def getDataByDataType(datatype, list):
    if 'sensorName' in list[0]:
        key = 'sensorName'
        aList = [ele for ele in list if ele[key] == 'acc']
        linList = [ele for ele in list if ele[key] == 'linacc']
        gList = [ele for ele in list if ele[key] == 'gyro']
    elif 'source' in list[0]:
        key = 'source'
        aList = [ele for ele in list if ele[key] == 'accelerator']
        # old log does not have fused linear acceleration
        gList = [ele for ele in list if ele[key] == 'Gyroscope']
    else:
        print 'wrong data src format, no sensorName or source in it'
        return None

    if(datatype == 'accelerator'):
        return aList
    elif(datatype == 'linacc'):
        return linList
    elif(datatype == 'gyro'):
        return gList
    else:
        print 'wrong data type:', datatype, ' must be either accelerator, linacc or gyro'
        return None


def readFile(filePath, isOld=False):
    with open(filePath) as f:
        jlist = [line.rstrip() for line in f]
        dataList = [json.loads(j) for j in jlist]
        if isOld:
            return dataList[0]
        else:
            return dataList

def readFiles(filePaths):
    dataList = []
    for path in filePaths:
        print path
        dataList.extend(readFile(path))
    return dataList

def splitDataListBySampleGranularity(granularity, dataList):
    return [dataList[i:i+granularity] for i in range(0, len(dataList), granularity)]

def splitDataListByStatus(dataList):
    buckets = {}
    for data in dataList:
        status = data['status']
        if status in buckets:
            buckets[status].append(data)
        else:
            buckets[status] = [data]

    return [buckets[key] for key in buckets]


def assignClassToBucket(buckets):
    y = []
    for bucket in buckets:
        data = bucket[0]
        status = data['status']
        y.append(STAT_CODE[status])
    return y

def processFile(filePaths, granularity):
    dataList = readFiles(filePaths)

    accList = getDataByDataType('accelerator', dataList)

    betterPrintData(accList)

    print 'len datalist:', len(dataList), ' len acclist:', len(accList)

    buckets = splitDataListByStatus(accList)

    slices = []
    for bucket in buckets:
        list = splitDataListBySampleGranularity(granularity, bucket)
        slices.extend(list)

    y = assignClassToBucket(slices)

    return slices, y

def printDataLables(filePath):
    statusCounter = {}
    dataList = readFile(filePath)
    for dt in dataList:
        status = dt['status']
        if status in statusCounter:
            statusCounter[status] += 1
        else:
            statusCounter[status] = 1
    print statusCounter

def betterPrint(filePath):
    dataList = readFile(filePath)
    betterPrintData(dataList)


def betterPrintData(dataList):
    message = ''
    dataList = getDataByDataType('accelerator', dataList)

    previousStatus = dataList[0]['status']

    message += (previousStatus + ' starts at:' + str(0))

    for i, dt in enumerate(dataList):
        status = dt['status']
        if status != previousStatus:
            message += str(' end at:' + str(i-1))
            message += str('|' + status + ' starts at:' + str(i))
            previousStatus = status

    message += str('end at:' + str(len(dataList)))

    print message


# betterPrint('/Users/jiusi/walkingandsitting1221.txt')
# betterPrint('/Users/jiusi/try.txt')
# betterPrint('/Users/jiusi/walking12130.txt')
# betterPrint('/Users/jiusi/shouldsmall.txt')
# betterPrint('/Users/jiusi/teststatus.txt')
# betterPrint('/Users/jiusi/ts1.txt')
# betterPrint('/Users/jiusi/run.txt')
# betterPrint('/Users/jiusi/doutui.txt')

def extractStatus(filePath, type, status, start, end):
    fileName = ntpath.basename(filePath)
    dirName = ntpath.dirname(filePath)
    outPath = dirName+'/'+fileName+'.rfn'
    print 'extract to:', outPath

    data = readFile(filePath)
    data = getDataByDataType(type, data)
    buckets = splitDataListByStatus(data)

    for bucket in buckets:
        if bucket[0]['status'] == status:
            data = bucket

    data = data[start:end]

    f = open(outPath, 'w')
    for d in data:
        f.write(json.dumps(d)+'\n')
    f.close()


def mergeFile(filePaths):
    dirName = ntpath.dirname(filePaths[0])
    outPath = dirName +'/merge.txt'
    print 'merge to:', outPath
    f = open(outPath, 'w')
    dataList = readFiles(filePaths)
    for dt in dataList:
        f.write(json.dumps(dt) + '\n')
    f.close()
