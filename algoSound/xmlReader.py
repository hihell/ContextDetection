__author__ = 'jiusi'

import xml.etree.ElementTree as ET
import parameters as param

def readXML(xmlPath):

    tree = ET.parse(xmlPath)
    root = tree.getroot()

    # key: class name, value: class id
    classDict = {}

    for classes in root.findall('classes'):
        for c in classes:
            classDict[c.text] = int(c.attrib['id'])

    # key: environment name, value: events, filePath and other info
    fileDict = {}

    for dataset in root.findall('dataset'):
        name = dataset[0].text
        fileNameLeft = dataset[1].text
        fileNameRight = dataset[2].text

        annotations = dataset[3]

        events = []
        for event in annotations.findall('event'):
            start = float(event[0].text)
            stop = float(event[1].text)
            type = event[2].text

            events.append({'start':start,
                           'stop':stop,
                           'type':type})

        fileDict[name] = {'events': events,
                          'fileNameLeft': fileNameLeft,
                          'fileNameRight': fileNameRight}

    return classDict, fileDict


# classDict, fileDict = readXML(param.xmlPath)
# print fileDict
# fileNames = [fileName for fileName in fileDict]
# for f in sorted(fileNames):
#     print f


