import sys
from editing.xmlPreprocessing import xmlTreeModifier
from amazonPollyTTS.convert import TTS
from amazonPollyTTS.getFiles import getAWSTTSFiles
if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("convert to speach")
    TTS(rootDir)


