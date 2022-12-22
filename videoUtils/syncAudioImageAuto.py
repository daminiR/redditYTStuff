import os
from collections import Counter
import json
from pydub import AudioSegment
from difflib import SequenceMatcher

def checkStructure(timestamps, redditFolder):
    timestamps = timestamps["ImageTimeStamps"]
    check_idx = 0
    for timestamp in timestamps:
        if "STORY" in timestamp["Mark Sentence"]:
            ## dont start new story if more than 20 minutes
            start = timestamp["Time"] / 1000
            duration = timestamp["Duration"] / 1000
            story_number = timestamp["Mark Sentence"].split("STORY")[1]
            txt_clip = "STORY" +  " " + story_number
        else:
            start = timestamp["Time"] / 1000
            duration = timestamp["Duration"] / 1000
            comment = redditFolder + "/screenshots/" + timestamp["Filename"]
        check_idx += 1

def calcualteDuration(jsonImageTime, redditFolder):
    originalVoiceOver = AudioSegment.from_mp3(redditFolder +  "/voiceOver/edited/eddited.mp3")
    end =  originalVoiceOver.duration_seconds * 1000
    newFinalJSon = {"ImageTimeStamps" : []}
    totalFiles =  len(jsonImageTime["ImageTimeStamps"])
    new =  jsonImageTime["ImageTimeStamps"]
    for index, matchDict in enumerate(jsonImageTime["ImageTimeStamps"]):
            if index  !=  totalFiles - 1:
                # if not isinstance(new[index + 1], list):
                    duration = jsonImageTime["ImageTimeStamps"][index + 1]["Time"] - matchDict["Time"]
                    matchDict["Duration"] = duration
            else:
                duration = end - matchDict["Time"]
                matchDict["Duration"] = duration
            newFinalJSon["ImageTimeStamps"].append(matchDict)
    return newFinalJSon


def syncAudioToImagesAutoShorts(redditFolder, videoType='long'):
    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []
    if videoType =="long":
        marks_bits = "marks_edited_with_bits.json"
        outTimeStamps = "screenshotTimestamps.json"
    else:
        marks_bits = "marks_edited_with_bits_shorts.json"
        outTimeStamps = "screenshotTimestamps_shorts.json"
    with open(redditFolder + "/marks/edited/" + marks_bits) as input, open(redditFolder + "/sync/" + outTimeStamps, "w+", encoding='utf8') as output:
        voiceOverMarks = json.load(input)
        edited = []
        long_comment = []
        long_idx_start = False
        long_idx_end = False
        idx = 0
        while idx < len(voiceOverMarks):
            mark = voiceOverMarks[idx]
            if  "LONG COMMENT START" in mark['value']:
                long_idx_start = idx
            if  "LONG COMMENT END" in mark['value']:
                long_idx_end = idx
                print(long_idx_start, long_idx_end)
                long_comment = voiceOverMarks[long_idx_start:long_idx_end]
                edited.append(long_comment)
                long_comment = []
                long_idx_start = False
                long_idx_end = False
            if "COMMENT" == mark['value']:
                edited.append(mark)
                edited.append(voiceOverMarks[idx + 1])
            elif "sentence" == mark['type'] or "TITLE" in mark['value'] or "STORY" in mark['value']:
                if long_idx_start == False and long_idx_end == False:
                    edited.append(mark)
            idx += 1
        sorted_idx = 0
        total_surplus = 0
        for idx, mark in enumerate(edited):
            if isinstance(mark, list):
                long = []
                new_idx = 0
                for val_idx, val in enumerate(mark):
                    if "PARA" == val['value']:
                        matchDict = {}
                        matchDict["Time"] = mark[val_idx]['time']
                        text = mark[val_idx + 1]['value']
                        matchDict["Filename"] = "screen_" + str(sorted_idx) + "_" + str(new_idx) + ".jpg"
                        matchDict["Mark Sentence"] = text
                        long.append(matchDict)
                        new_idx += 1
                total_surplus += len(mark) + 1
                jsonImageTime["ImageTimeStamps"].extend(long)
                sorted_idx += 1
            else:
                if 'STORY' in mark['value']:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = mark['value']
                    matchDict["Filename"] = None
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
                elif "COMMENT" == mark['value']:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = edited[idx + 1]['value'][:25]
                    matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                    sorted_idx += 1
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
                # elif idx == 0 and not isinstance(mark, list):
                elif idx == 0 and not isinstance(edited[idx + 1], list):
                # elif idx == 0:
                    print(mark)
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = "TITLE"
                    matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                    sorted_idx += 1
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
        newFinal = calcualteDuration(jsonImageTime, redditFolder)
        checkStructure(newFinal, redditFolder)
        json.dump(newFinal, output, indent=4)

def syncAudioToImagesAuto(redditFolder, videoType='long'):
    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []
    if videoType =="long":
        marks_bits = "marks_edited_with_bits.json"
        outTimeStamps = "screenshotTimestamps.json"
    else:
        marks_bits = "marks_edited_with_bits_shorts.json"
        outTimeStamps = "screenshotTimestamps_shorts.json"
    with open(redditFolder + "/marks/edited/" + marks_bits) as input, open(redditFolder + "/sync/" + outTimeStamps, "w+", encoding='utf8') as output:
        voiceOverMarks = json.load(input)
        edited = []
        long_comment = []
        long_idx_start = False
        long_idx_end = False
        idx = 0
        while idx < len(voiceOverMarks):
            mark = voiceOverMarks[idx]
            if  "LONG COMMENT START" in mark['value']:
                long_idx_start = idx
            if  "LONG COMMENT END" in mark['value']:
                long_idx_end = idx
                print(long_idx_start, long_idx_end)
                long_comment = voiceOverMarks[long_idx_start:long_idx_end]
                edited.append(long_comment)
                long_comment = []
                long_idx_start = False
                long_idx_end = False
            if "COMMENT" == mark['value']:
                edited.append(mark)
                edited.append(voiceOverMarks[idx + 1])
            elif "sentence" == mark['type'] or "TITLE" in mark['value'] or "STORY" in mark['value']:
                if long_idx_start == False and long_idx_end == False:
                    edited.append(mark)
            idx += 1
        sorted_idx = 0
        total_surplus = 0
        for idx, mark in enumerate(edited):
            if isinstance(mark, list):
                long = []
                new_idx = 0
                print(mark)
                for val_idx, val in enumerate(mark):
                    if "PARA" == val['value']:
                        matchDict = {}
                        matchDict["Time"] = mark[val_idx]['time']
                        text = mark[val_idx + 1]['value']
                        matchDict["Filename"] = "screen_" + str(sorted_idx) + "_" + str(new_idx) + ".jpg"
                        matchDict["Mark Sentence"] = text
                        long.append(matchDict)
                        new_idx += 1
                total_surplus += len(mark) + 1
                jsonImageTime["ImageTimeStamps"].extend(long)
                sorted_idx += 1
            else:
                if 'STORY' in mark['value']:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = mark['value']
                    matchDict["Filename"] = None
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
                elif "COMMENT" == mark['value']:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = edited[idx + 1]['value'][:25]
                    matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                    sorted_idx += 1
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
                elif idx == 0 and not isinstance(edited[idx + 1], list):
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = "TITLE"
                    matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                    sorted_idx += 1
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
        newFinal = calcualteDuration(jsonImageTime, redditFolder)
        checkStructure(newFinal, redditFolder)
        json.dump(newFinal, output, indent=4)
