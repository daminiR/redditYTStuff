from moviepy.editor import *
from moviepy.editor import VideoFileClip
from moviepy.video import *
from moviepy.audio import *
from moviepy.audio.AudioClip import AudioClip
import moviepy
import numpy as np
from pydub import AudioSegment
import os, random
import json
from moviepy.video.fx.all import crop

def createShorts(redditFolder):
    desired_length = 58 # 20 sh min
    # choose random video from collection
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollectionShorts/SnapSave.io-Minecraft Gameplay - Free To Use Gameplay.mov"
    videoPath=videoCollection
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited_shorts.mp3")
    new_audioclip = originalVoiceOver
    comments = []
    with open(redditFolder + "/sync/screenshotTimestamps_shorts.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        check_idx = 0
        for timestamp in timestamps:
                if timestamp["Time"] / 1000 > desired_length:
                    actual_length = timestamp["Time"] / 1000
                    break
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                print(timestamp["Filename"])
                comment = ImageClip(redditFolder + "/screenshots_shorts/" + timestamp["Filename"]).set_start(start).set_duration(duration).set_pos(("center","center"))
                if comment.size[1] > backgroundVideoSize[1]:
                    resizeComment = comment.resize((int(backgroundVideoSize[0] * 0.8), int(backgroundVideoSize[1])*0.95))
                else:
                    resizeComment = comment.resize(width=int(backgroundVideoSize[0] * 0.9))
                comments.append([resizeComment, start + duration])
                check_idx += 1
        pause = 2
        while actual_length > 58:
            comments = comments[:-1]
            actual_length = comments[-1][1]
        new_audioclip = new_audioclip.subclip(0, actual_length + 0.5)
        cliped_duration = new_audioclip.duration
        loopedVideo = backgroundVideo.loop(duration=cliped_duration + pause)
        only_comments = [x[0]  for x in comments]
        final = CompositeVideoClip([loopedVideo, *only_comments])
        # final = CompositeVideoClip([*comments])
        # all audio
        ######################################
        final.audio = new_audioclip
        ######################################
        # final = final.resize(0.3)
        # final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video.mp4",codec='hevc_videotoolbox', fps=24)
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_shorts.mp4")
