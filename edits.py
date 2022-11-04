import sys
from editing.addAutoAudioEffects import audioEdits
from amazonPollyTTS.getFiles import getAWSTTSFiles
from utils.convertXMLtoJSON import converToJSON
if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("get amazon polly files")
    getAWSTTSFiles(rootDir)
    print("convert masks to proper json")
    converToJSON(rootDir)
    print("edit audio for effects")
    audioEdits(rootDir)





