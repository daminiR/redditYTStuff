import sys
from videoUtils.createVideo import createVideo
from utils.edit_thumnail import createThumbnail

if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("create audio")
    createVideo(rootDir)
