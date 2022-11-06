from moviepy.editor import *

def createVideo(redditFolder):
    video = VideoFileClip("/home/damini/Downloads/Veil - 66423.mp4")

    title = ImageClip("redditFolder" + "/screenshots/Screenshot from 2022-11-04 22-06-06.png").set_start(3).set_duration(7).set_pos(("center","center"))
              #.resize(height=50) # if you need to resize...


    final = CompositeVideoClip([video, title])
    final.write_videofile("./test.mp4")
