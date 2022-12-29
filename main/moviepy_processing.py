import sys
from videoUtils.createVideo import createVideo
from videoUtils.createShorts import createShorts
from utils.edit_thumnail import createThumbnail

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoType = sys.argv[2]
    desired_length = 15
    if videoType == 'short':
            print("create short audio")
            createShorts(rootDir)
    elif videoType == 'long':
        if len(sys.argv) == 4:
            print("create long audio")
            desired_length = int(sys.argv[3])
            createVideo(rootDir, desired_length)
