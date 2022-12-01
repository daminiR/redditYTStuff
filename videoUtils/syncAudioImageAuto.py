import os
from collections import Counter
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

def syncAudioToImagesAuto(redditFolder):
    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []
    with open(redditFolder + "/marks/edited/marks_edited_with_bits.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+", encoding='utf8') as output:
        voiceOverMarks = json.load(input)
        sorted_idx = 0
        long_idx = 0
        for idx, mark in enumerate(voiceOverMarks):
            if 'STORY' in mark['value']:
                if long_idx != 0:
                    sorted_idx += 1
                    long_idx = 0
                matchDict = {}
                matchDict["Time"] = mark['time']
                text = mark['value']
                matchDict["Filename"] = None
                jsonImageTime["ImageTimeStamps"].append(matchDict)
                matchDict["Mark Sentence"] = text
            elif "COMMENT" == mark['value'] and "LONG COMMENT" != voiceOverMarks[idx + 1]['value']:
                if long_idx != 0:
                    long_idx = 0
                matchDict = {}
                matchDict["Time"] = mark['time']
                text = voiceOverMarks[idx + 1]['value'][:25]
                matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                sorted_idx += 1
                jsonImageTime["ImageTimeStamps"].append(matchDict)
                matchDict["Mark Sentence"] = text
            if 'LONG COMMENT' == mark['value']:
                matchDict = {}
                matchDict["Time"] = mark['time']
                text = voiceOverMarks[idx + 1]['value'][:25]
                matchDict["Filename"] = "screen_" + str(sorted_idx)+  "_" + str(long_idx) + ".jpg"
                long_idx += 1
                jsonImageTime["ImageTimeStamps"].append(matchDict)
                matchDict["Mark Sentence"] = text
        newFinal = calcualteDuration(jsonImageTime, redditFolder)
        json.dump(newFinal, output, indent=4)


