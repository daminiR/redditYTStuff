import os
import json
from pydub import AudioSegment
from difflib import SequenceMatcher

def calcualteDuration(jsonImageTime, redditFolder):
    originalVoiceOver = AudioSegment.from_mp3(redditFolder +  "/voiceOver/edited/eddited.mp3")
    end =  originalVoiceOver.duration_seconds * 1000
    newFinalJSon = {"ImageTimeStamps" : []}
    totalFiles =  len(jsonImageTime["ImageTimeStamps"])
    for index, matchDict in enumerate(jsonImageTime["ImageTimeStamps"]):
        if index  !=  totalFiles - 1:
            duration = jsonImageTime["ImageTimeStamps"][index + 1]["Time"] - matchDict["Time"]
            matchDict["Duration"] = duration
        else:
            duration = end - matchDict["Time"]
            matchDict["Duration"] = duration
        newFinalJSon["ImageTimeStamps"].append(matchDict)
    return newFinalJSon

def syncAudioToImages(redditFolder):
    subReddit = "r/AskReddit"

    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []

    with open(redditFolder + "/screenShotIds/tastIds.json", "r") as f:
        taskIDs = json.load(f)["TaskIds"]

    with open(redditFolder + "/marks/edited/marks_edited_with_bits.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+") as output:
        voiceOverMarks = json.load(input)
        for idx, mark in enumerate(voiceOverMarks):
            if 'STORY' in mark['value']:
                matchDict = {}
                matchDict["Time"] = mark['time']
                text = mark['value']
                matchDict["Filename"] = None
                matchDict["TaskId"] = None
                matchDict["Mark Sentence"] = text
                jsonImageTime["ImageTimeStamps"].append(matchDict)

            if 'COMMENT' in mark['value'] or idx ==0:
                matchDict = {}
                matchDict["Time"] = mark['time']
                if idx == 0:
                    text = voiceOverMarks[idx]['value']
                else:
                    text = voiceOverMarks[idx + 1]['value']
                compareTextA = " ".join(text.split(" ")[:7])
                closest = 0
                closestFile = None
                closestSentence = None
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
        newFinal = calcualteDuration(jsonImageTime, redditFolder)
        json.dump(jsonImageTime, output, indent=4)




