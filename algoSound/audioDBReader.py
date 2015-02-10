__author__ = 'jiusi'

import xml.etree.ElementTree as ET
import json

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

def readJson(jsonPath):

    print 'loading audio dir structure from:', jsonPath

    with open(jsonPath,'r') as f:
        root =  json.load(f)

        classDict = {}
        for cls in root['datasets']['classes']['class']:
            classDict[cls['__text']] = int(cls['_id'])

        fileDict = {}
        for dataset in root['datasets']['dataset']:
            name = dataset['name']
            fileNameLeft = None
            fileNameRight = None
            events = []

            for fileName in dataset['filename']:
                if 'left' in fileName['__text']:
                    fileNameLeft = fileName['__text']
                elif 'right' in fileName['__text']:
                    fileNameRight = fileName['__text']

            if 'annotations' in dataset:
                if 'event' in dataset['annotations']:
                    for event in dataset['annotations']['event']:
                        tmp = {}
                        tmp['start'] = float(event['start'])
                        tmp['stop'] = float(event['stop'])
                        tmp['type'] = event['type']

                        events.append(tmp)

            fileDict[name] = {
                'events': events,
                'fileNameLeft': fileNameLeft,
                'fileNameRight': fileNameRight
            }

        return classDict, fileDict

