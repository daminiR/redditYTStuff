import sys
from editing.addAutoAudioEffects import audioEdits
from amazonPollyTTS.getFiles import getAWSTTSFiles
from utils.convertXMLtoJSON import converToJSON
if __name__ == "__main__":
    rootDir = sys.argv[1]
    # getAWSTTSFiles(rootDir)
    converToJSON(rootDir)
    # audioEdits(rootDir)





