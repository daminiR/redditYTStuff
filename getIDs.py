import sys
from amazonTextract.exract import extractTextIds
# from amazonTextract.syncAudioImage import syncAudioToImages
if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("getting img task Ids")
    extractTextIds(rootDir)
    # print("getting img task Ids")
    # syncAudioToImages(rootDir)


