__author__ = 'jiusi'

import utilsData as ud
import utilsPlot as up
import json
import ntpath

def plotFile(filePath, sensor):
    data = ud.readFile(filePath)
    senData = ud.getDataBySensorType(sensor, data)
    ud.betterPrintData(senData)
    up.plotLines(senData, [0,1,2], title=filePath)

def extractDataFromFile(filePath, sensor, start, end):
    plotFile(filePath, sensor)

    fileName = ntpath.basename(filePath)
    dirName = ntpath.dirname(filePath)
    outPath = dirName+'/'+fileName+'.rfn'
    print 'extract to:', outPath

    data = ud.readFile(filePath)
    data = ud.getDataBySensorType(sensor, data)

    data = data[start:end]

    f = open(outPath, 'w')
    for d in data:
        f.write(json.dumps(d)+'\n')
    f.close()

    plotFile(outPath, sensor)

def mergeFile(filePaths, sensor):

    if len(filePaths) != 2:
        print 'should pass 2 files to this function', filePaths
        return

    plotFile(filePaths[0], sensor)

    dirName = ntpath.dirname(filePaths[0])
    outPath = dirName +'/merge.txt'
    print 'will append:', filePaths[1], ' to:', filePaths[0], ' result in:',outPath

    f = open(outPath, 'w')
    dataList = ud.readFiles(filePaths)
    for dt in dataList:
        f.write(json.dumps(dt) + '\n')
    f.close()

    plotFile(outPath, sensor)


def removeNoise(filePath, noiseLocations, sensor='accelerometer'):

    plotFile(filePath, sensor)

    rawList = ud.readFile(filePath)
    rawList = ud.getDataBySensorType(list=rawList, datatype=sensor)

    fileName = ntpath.basename(filePath)
    dirName = ntpath.dirname(filePath)
    outPath = dirName+'/'+fileName+'.rfn'

    print 'total length of ', sensor, ' data is:', len(rawList)
    print 'noise is located at:', noiseLocations
    print 'refined data will be saved in:', outPath

    dataList = []
    noise = noiseLocations.pop(0)
    for i in range(0, len(rawList)):
        if i < noise[0] or i > noise[1]:
            dataList.append(rawList[i])

        if i >= noise[1]:
            if len(noiseLocations) > 0:
                noise = noiseLocations.pop(0)

    f = open(outPath, 'w')
    for d in dataList:
        f.write(json.dumps(d)+'\n')
    f.close()

    plotFile(outPath, sensor)
