from moviepy.editor import *
from moviepy.video import *
from moviepy.audio import *
from pydub import AudioSegment
import json

def createVideo(redditFolder):
    video = VideoFileClip("/Users/daminirijhwani/Downloads/Background - 13949.mp4")
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited.mp3")
    # audioclip = AudioFileClip("audioname.mp3")
    new_audioclip = CompositeAudioClip([originalVoiceOver])
    end =  originalVoiceOver.duration
    print("total video", end)
    loopedVideo = video.loop(duration= end + 10)

    # title = ImageClip(redditFolder + "/screenshots/Screenshot from 2022-11-04 22-06-06.png").set_start(3).set_duration(7).set_pos(("center","center"))
    # final = CompositeVideoClip([video, title])
    # final.write_videofile("./test.mp4")
    comments = []
    with open(redditFolder + "/sync/screenshotTimestamps.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        for timestamp in timestamps:
            print("file: ", timestamp["Filename"])
            start = timestamp["Time"] / 1000
            duration = timestamp["Duration"] / 1000
            comment = ImageClip(redditFolder + "/screenshots/" + timestamp["Filename"] + ".png").set_start(start).set_duration(duration).set_pos(("center","center"))
            comments.append(comment)

        final = CompositeVideoClip([loopedVideo, *comments])
        final.audio = new_audioclip
        final.write_videofile("./test.mp4")

