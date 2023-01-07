import sys
from editing.addAutoAudioEffects import audioEdits
from amazonPollyTTS.getFiles import getAWSTTSFiles
from utils.convertXMLtoJSON import converToJSON
from videoUtils.syncAudioImageAuto import syncAudioToImagesAuto, syncAudioToImagesAutoShorts

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoType = sys.argv[2]
    if videoType == 'tiktok':
        print("get amazon polly files")
        getAWSTTSFiles(rootDir, videoType)
        print("convert masks to proper json")
        converToJSON(rootDir,videoType)
        print("edit audio for effects")
        audioEdits(rootDir, videoType)
        print("getting img task Ids")
        syncAudioToImagesAutoShorts(rootDir, videoType)
    if videoType == 'short':
        print("get amazon polly files")
        getAWSTTSFiles(rootDir, videoType)
        print("convert masks to proper json")
        converToJSON(rootDir,videoType)
        print("edit audio for effects")
        audioEdits(rootDir, videoType)
        print("getting img task Ids")
        syncAudioToImagesAutoShorts(rootDir, videoType)
    elif videoType == 'long':
        print("get amazon polly files")
        getAWSTTSFiles(rootDir, videoType)
        print("convert masks to proper json")
        converToJSON(rootDir,videoType)
        print("edit audio for effects")
        audioEdits(rootDir, videoType)
        print("getting img task Ids")
        syncAudioToImagesAuto(rootDir)





