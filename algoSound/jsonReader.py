__author__ = 'jiusi'

import json

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