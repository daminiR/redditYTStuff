import sys
from videoUtils.createVideo import createVideo
from videoUtils.createShorts import createShorts
from utils.edit_thumnail import createThumbnail

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoType = sys.argv[2]
    if len(sys.argv) == 3:
        speed = sys.argv[3]
    if videoType == 'short':
        print("create short audio")
        createShorts(rootDir, speed)
    elif videoType == 'long':
        print("create long audio")
        createVideo(rootDir)
