import sys
from videoUtils.syncAudioImageAuto import syncAudioToImagesAuto

if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("getting img task Ids")
    syncAudioToImagesAuto(rootDir)




