import sys
from amazonPollyTTS.convert import TTS
from utils.pdfSplit import generateScreensSSML

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoType = sys.argv[2]
    print("convert to speach")
    if videoType == 'short':
        TTS(rootDir, "short")
    elif videoType == 'long':
        TTS(rootDir, "long")
    elif videoType == 'tiktok':
        TTS(rootDir, "tiktok")


