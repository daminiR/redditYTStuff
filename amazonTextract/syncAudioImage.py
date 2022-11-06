import os
import json
from pydub import AudioSegment
from difflib import SequenceMatcher
# def searchTaskIds(taskIDs):
def calcualteDuration(jsonImageTime):
    newFinalJSon = {"ImageTimeStamps" : []}
    totalFiles =  len(jsonImageTime["ImageTimeStamps"])
    for index, matchDict in enumerate(jsonImageTime["ImageTimeStamps"]):
        if index  !=  totalFiles - 1:
            duration = jsonImageTime["ImageTimeStamps"][index + 1]["Time"] - matchDict["Time"]
            matchDict["Duration"] = duration
            newFinalJSon["ImageTimeStamps"].append(matchDict)
        # else:
    return newFinalJSon

def syncAudioToImages(redditFolder):

    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []

    with open(redditFolder + "/screenShotIds/tastIds.json", "r") as f:
        taskIDs = json.load(f)["TaskIds"]

    with open(redditFolder + "/marks/edited/marks_processed.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+") as output:
        voiceOverMarks = json.load(input)
        for idx, mark in enumerate(voiceOverMarks):
            if 'COMMENT' in mark['value']:
                matchDict = {}
                matchDict["Time"] = mark['time']
                text = voiceOverMarks[idx + 1]['value']
                compareTextA = " ".join(text.split(" ")[:7])
                closest = 0
                closestFile = None
                closestSentence = None
                # print(taskIDs)
                for id in taskIDs:
                    compareTextB = id["TaskId"]
                    sequenceRatio = SequenceMatcher(None, compareTextA, compareTextB).ratio()
                    if closest < sequenceRatio:
                        closest = sequenceRatio
                        closestFile = id["File"]
                        closestSentence = id["TaskId"]
                matchDict["Filename"] = closestFile
                matchDict["TaskId"] = closestSentence
                matchDict["Mark Sentence"] = compareTextA

                jsonImageTime["ImageTimeStamps"].append(matchDict)
        newFinal = calcualteDuration(jsonImageTime)
        json.dump(jsonImageTime, output, indent=4)




