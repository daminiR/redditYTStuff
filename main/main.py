import sys
from amazonPollyTTS.convert import TTS
from utils.pdfSplit import generateScreensSSML

if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("convert to speach")
    TTS(rootDir)


