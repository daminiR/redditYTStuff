import sys
from amazonTextract.exract import extractTextIds
from amazonTextract.syncAudioImage import syncAudioToImages
from amazonTextract.syncAudioImageAuto import syncAudioToImagesAuto
from amazonTextract.createVideo import createVideo


if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("getting img task Ids")
    # extractTextIds(rootDir)
    # print("getting img task Ids")
    # syncAudioToImages(rootDir)
    syncAudioToImagesAuto(rootDir)




