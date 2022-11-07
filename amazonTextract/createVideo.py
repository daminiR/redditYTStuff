from moviepy.editor import *
from moviepy.video import *
from moviepy.audio import *
from moviepy.video.fx.resize import resize
from pydub import AudioSegment
import json

def createVideo(redditFolder):
    titleVideo = VideoFileClip("/Users/daminirijhwani/Downloads/Park - 6096.mp4")
    backgroundVideo = VideoFileClip("/Users/daminirijhwani/Downloads/Background - 13949.mp4")
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited.mp3")
    new_audioclip = CompositeAudioClip([originalVoiceOver])
    end = originalVoiceOver.duration
    loopedVideo = backgroundVideo.loop(duration=end + 10)
    backgroundVideoSize = backgroundVideo.size
    comments = []

    with open(redditFolder + "/sync/screenshotTimestamps.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        for timestamp in timestamps:
            if "STORY" not in timestamp["Mark Sentence"]:
                print("file: ", timestamp["Filename"])
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                comment = ImageClip(redditFolder + "/screenshots/" + timestamp["Filename"] + ".png").set_start(start).set_duration(duration).set_pos(("center","center"))
                resizeComment = comment.resize(0.7)
                comments.append(resizeComment)
            else:
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                story_number = timestamp["Mark Sentence"].split("STORY")[1]
                txt_clip = TextClip("STORY" +  " " + story_number, fontsize=75, font="Amiri-bold", color='white', bg_color='gray', stroke_color='black',stroke_width=2.5).set_start(start).set_duration(duration).set_pos("center")
                comments.append(txt_clip)

        untilTitle = int(timestamps[1]["Time"] / 1000)
        if titleVideo.duration > untilTitle:
            titleclip = titleVideo.subclip(0, untilTitle)

        finalBackround = concatenate_videoclips([titleclip, loopedVideo])
        final = CompositeVideoClip([finalBackround, *comments])
        final.audio = new_audioclip
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video.mp4")

