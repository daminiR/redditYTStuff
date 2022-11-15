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

def syncAudioToImages(redditFolder):
    subReddit = "r/AskReddit"

    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []

    with open(redditFolder + "/screenShotIds/tastIds.json", "r") as f:
        taskIDs = json.load(f)["TaskIds"]


    log_errors = redditFolder + "/sync/errors/duplicates.json"
    with open(redditFolder + "/marks/edited/marks_edited_with_bits.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+", encoding='utf8') as output:
        voiceOverMarks = json.load(input)
        req_marks = len([mark for mark in voiceOverMarks if "COMMENT" in mark["value"]]) + 1
        current_screens = len(taskIDs)
        # if req_marks != current_screens:
            # raise Exception("cant conitnue until screens are the same! you need {} screenshots, you have {} screens", req_marks, current_screens)
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
                ### for title
                if idx == 0:
                    text = voiceOverMarks[idx]['value']
                    for id in taskIDs:
                        if subReddit in id["TaskId"]:
                            matchDict["Filename"] = id["File"]
                            matchDict["TaskId"] = mark["value"]
                            matchDict["Mark Sentence"] = mark["value"]
                            matchDict["Confidence"] = 1
                            break
                else:
                    text = voiceOverMarks[idx + 1]['value'] + voiceOverMarks[idx + 2]['value']
                    compareTextA = " ".join(text.split(" ")[:7])
                    closest = 0
                    closestFile = None
                    closestSentence = None
                    for id in taskIDs:
                        if subReddit in id["TaskId"]:
                            pass
                        compareTextB = id["TaskId"]
                        sequenceRatio = SequenceMatcher(None, compareTextA, compareTextB).ratio()
                        if closest < sequenceRatio:
                            closest = sequenceRatio
                            closestFile = id["File"]
                            closestSentence = id["TaskId"]
                    matchDict["Filename"] = closestFile
                    matchDict["TaskId"] = closestSentence
                    matchDict["Mark Sentence"] = compareTextA
                    matchDict["Confidence"] = closest
                jsonImageTime["ImageTimeStamps"].append(matchDict)
        newFinal = calcualteDuration(jsonImageTime, redditFolder)
         ## check for duplicates screens attached in task ids!
        dict_freq = {}
        for value in newFinal["ImageTimeStamps"]:
            if value["Filename"] in dict_freq:
                dict_freq[value["Filename"]][0] += 1
                dict_freq[value["Filename"]][1].append(value)
            else:
                dict_freq[value["Filename"]] = [1, [value] ]
        duplicates = {"Duplicates" : [value[1] for key, value in dict_freq.items() if value[0] > 1 and key != None]}
        if len(duplicates) > 0:
            # print(*duplicates, sep = "\n")
            ### important try to remove duplicate if exits in screnshots so you dont have to manually!!
            final_dups = {"Duplicates" :[]}
            for duplicate in duplicates["Duplicates"]:
                values = duplicate
                bestConf = 0
                bestFile = None
                for each_value in values:
                    print(each_value)
                    if float(each_value["Confidence"]) > bestConf:
                        bestConf = float(each_value["Confidence"])
                        bestFile = each_value["Filename"]
                # remove all files except best
                for each_value in values:
                    if each_value["Filename"] != bestFile:
                        if os.path.exists(redditFolder + "/screnshots/" + each_value["Filename"]):
                            os.remove.exists(redditFolder + "/screnshots/" + each_value["Filename"])
                            each_value["Status"] = "File deleted"
                        else:
                            each_value["Status"] = "File not deleted or doesnt exists"
            with open(log_errors, "w+") as error_file:
                json.dump(duplicates, error_file, indent=4)
            # raise Exception("There are duplicates!!")
        json.dump(newFinal, output, indent=4)
