from moviepy.editor import *

def createVideo(redditFolder):
    video = VideoFileClip(redditFolder + "/sync/screenshotTimestamps.js")

    title = ImageClip("title.png").set_start(3).set_duration(7).set_pos(("center","center"))
              #.resize(height=50) # if you need to resize...


    final = CompositeVideoClip([video, title])
    final.write_videofile("test.mp4")
