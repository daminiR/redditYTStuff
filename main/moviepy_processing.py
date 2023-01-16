import sys
from videoUtils.createVideo import createVideo
from videoUtils.createShorts import createShorts
from videoUtils.createTiktoks import createTiktoks
from utils.edit_thumnail import createThumbnail

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoType = sys.argv[2]
    desired_length = 15
    if videoType == 'short':
            print("create short audio")
            createShorts(rootDir)
    if videoType == 'tiktok':
            videoLength = int(sys.argv[3])
            print("create tiktok audio")
            if videoLength < 60:
                videoName = "shorts"
            else:
                videoName = "tiktok"
            createTiktoks(rootDir, videoLength, videoName)
    elif videoType == 'long':
        if len(sys.argv) == 4:
            print("create long audio")
            desired_length = int(sys.argv[3])
            print(desired_length)
            createVideo(rootDir, desired_length)
