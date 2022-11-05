import os
import json
from pydub import AudioSegment


# def searchTaskIds(taskIDs):


def syncAudioToImages(redditFolder):
    with open(redditFolder + "/screenShotIds/tastIds.json", "r") as f:
        taskIDs = json.load(f)

    with open(redditFolder + "/marks/edited/marks_processed.json") as input, open(redditFolder + "/sync/screenshotTimestamps.json", "w+"):
        voiceOverMarks = json.load(input)
        for mark in voiceOverMarks:
            # if 'sentence' in mark['type'] and first_sentence==0:
                # metaDataDict['RedditTitle'] = mark['value']
                # print(metaDataDict)
                # handle = open(metadataFile, 'w')
                # first_sentence=1
                # json.dump(metaDataDict, handle)
                # handle.close()

            if 'COMMENT' in mark['value']:
                # time for new json value
                searchTaskIds()


