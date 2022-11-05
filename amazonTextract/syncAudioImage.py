import os
import json
from pydub import AudioSegment
from difflib import SequenceMatcher
# def searchTaskIds(taskIDs):
def syncAudioToImages(redditFolder):
    with open(redditFolder + "/screenShotIds/tastIds.json", "r") as f:
        taskIDs = json.load(f)["TaskIds"]

    with open(redditFolder + "/marks/edited/marks_processed.json") as input:
    # open(redditFolder + "/sync/screenshotTimestamps.json", "w+"):
        voiceOverMarks = json.load(input)
        for idx, mark in enumerate(voiceOverMarks):
            # if 'sentence' in mark['type'] and first_sentence==0:
                # metaDataDict['RedditTitle'] = mark['value']
                # print(metaDataDict)
                # handle = open(metadataFile, 'w')
                # first_sentence=1
                # json.dump(metaDataDict, handle)
                # handle.close()

            if 'COMMENT' in mark['value']:
                # time for new json value
                # search the second line of the marks for any matches
                text = voiceOverMarks[idx + 1]['value']
                compareTextA = " ".join(text.split(" ")[:7])
                closest = 0
                closestFile = None
                # print(taskIDs)
                for id in taskIDs:
                    compareTextB = id["TaskId"]
                    sequenceRatio = SequenceMatcher(None, compareTextA, compareTextB).ratio()
                    if closest < sequenceRatio:
                        closest = sequenceRatio
                        closestFile = id["File"]
                    # closest = max(closest,
                print("check match")
                print(compareTextA, closestFile)
                # searchTaskIds()


