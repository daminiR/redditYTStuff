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

def syncAudioToImagesAuto(redditFolder):
    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []
    with open(redditFolder + "/marks/edited/marks_edited_with_bits.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+", encoding='utf8') as output:
        voiceOverMarks = json.load(input)
        edited = []
        long_comment = []
        long_idx_start = None
        long_idx_end = None
        edited_map = {}
        for idx, mark in enumerate(voiceOverMarks):
            # print(mark)
            # if idx == 3:
                # return
            if 'STORY' in mark['value'] or "COMMENT" == mark['value'] or "TITLE" == mark['value']:
                if long_idx_start != None and long_idx_end != None:
                        long_comment = voiceOverMarks[long_idx_start:long_idx_end]
                        edited.append(long_comment)
                        long_idx_start = None
                        long_idx_end = None
                        long_comment = []
                if "COMMENT" == mark['value']:
                    edited.append(mark)
                    print(voiceOverMarks[idx + 1])
                    edited.append(voiceOverMarks[idx + 1])
                else:
                    edited.append(mark)
            elif 'LONG COMMENT START' in mark['value']:
                long_idx_start = idx
            elif 'LONG COMMENT END' in mark['value']:
                long_idx_end = idx

        sorted_idx = 0
        long_idx = 0
        last_time = 0
        total_surplus = 0
        for idx, mark in enumerate(edited):
            # if idx == 1:
                # break
            if isinstance(mark, list):
                last_time = mark[-1]['end']
                long = []
                new_idx = 0
                print(len(mark))
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
                elif idx == 0:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = "TITLE"
                    matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                    sorted_idx += 1
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                    matchDict["Mark Sentence"] = text
        newFinal = calcualteDuration(jsonImageTime, redditFolder)
        json.dump(jsonImageTime, output, indent=4)
