import sys
from videoUtils.createVideo import createVideo
from videoUtils.createShorts import createShorts
from utils.edit_thumnail import createThumbnail

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoType = sys.argv[2]
    if videoType == 'short':
            print("create short audio")
            createShorts(rootDir)
    elif videoType == 'long':
        print("create long audio")
        createVideo(rootDir)
