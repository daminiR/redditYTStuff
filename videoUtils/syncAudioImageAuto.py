import os
from collections import Counter
import json
from pydub import AudioSegment
from difflib import SequenceMatcher

# def calcualteDuration(jsonImageTime, redditFolder):
    # originalVoiceOver = AudioSegment.from_mp3(redditFolder +  "/voiceOver/edited/eddited.mp3")
    # end =  originalVoiceOver.duration_seconds * 1000
    # newFinalJSon = {"ImageTimeStamps" : []}
    # new =  jsonImageTime["ImageTimeStamps"]
    # for index, matchDict in enumerate(new):
        # if not isinstance(matchDict, list) and not isinstance(new[index + 1], list):
        # if isinstance(matchDict, list):
            # newFinalJSon["ImageTimeStamps"].append(long)
    # return newFinalJSon

def syncAudioToImagesAuto(redditFolder):
    jsonImageTime = {}
    jsonImageTime["ImageTimeStamps"] = []
    with open(redditFolder + "/marks/edited/marks_edited_with_bits.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+", encoding='utf8') as output:
        voiceOverMarks = json.load(input)
        edited = []
        long_comment = []
        long_idx_start = None
        long_idx_end = None
        for idx, mark in enumerate(voiceOverMarks):
            # if idx == 31:
                # break
            if 'STORY' in mark['value'] or "COMMENT" == mark['value']:
                if long_idx_start != None and long_idx_end != None:
                        long_comment = voiceOverMarks[long_idx_start:long_idx_end]
                        edited.append(long_comment)
                        long_idx_start = None
                        long_idx_end = None
                        long_comment = []
                edited.append(mark)
            elif 'LONG COMMENT START' in mark['value']:
                long_idx_start = idx
            elif 'LONG COMMENT END' in mark['value']:
                long_idx_end = idx
        sorted_idx = 0
        long_idx = 0
        for idx, mark in enumerate(edited):
            if isinstance(mark, list):
                long = []
                new_idx = 0
                for val_idx, val in enumerate(mark):
                    if "PARA" in val['value']:
                        matchDict = {}
                        matchDict["Time"] = mark[val_idx]['time']
                        text = mark[val_idx + 1]['value']
                        matchDict["Filename"] = "screen_" + str(sorted_idx) + "_" + str(new_idx) + ".jpg"
                        matchDict["Mark Sentence"] = text
                        matchDict["duration"] = mark[val_idx + 1]['end'] - mark[val_idx + 1]['start']
                        long.append(matchDict)
                        new_idx += 1
                jsonImageTime["ImageTimeStamps"].append(long)
            else:
                if 'STORY' in mark['value']:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = mark['value']
                    matchDict["Filename"] = None
                    matchDict["Mark Sentence"] = text
                    matchDict["duration"] = mark['end'] - mark['start']
                    jsonImageTime["ImageTimeStamps"].append(matchDict)
                elif "COMMENT" == mark['value']:
                    matchDict = {}
                    matchDict["Time"] = mark['time']
                    text = voiceOverMarks[idx + 1]['value'][:25]
                    matchDict["Filename"] = "screen_" + str(sorted_idx) + ".jpg"
                    matchDict["duration"] = mark['end'] - mark['start']
                    sorted_idx += 1
                    matchDict["Mark Sentence"] = text
                    jsonImageTime["ImageTimeStamps"].append(matchDict)

        json.dump(jsonImageTime, output, indent=4)
