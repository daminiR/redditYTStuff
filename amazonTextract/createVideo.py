from moviepy.editor import *
import json

def createVideo(redditFolder):
    video = VideoFileClip("/Users/daminirijhwani/Downloads/Background - 13949.mp4")
    # title = ImageClip(redditFolder + "/screenshots/Screenshot from 2022-11-04 22-06-06.png").set_start(3).set_duration(7).set_pos(("center","center"))
    # final = CompositeVideoClip([video, title])
    # final.write_videofile("./test.mp4")
    with open(redditFolder + "/sync/screenshotTimestamps.json") as f:
        timestamps = json.load(f)
        comment = ImageClip(redditFolder + "/screenshots/Screenshot from 2022-11-04 22-06-06.png").set_start(3).set_duration(7).set_pos(("center","center"))

