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
    speed = 1
    desired_duration = speed * 40
    # choose random video from collection
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollectionShorts/"
    filename = random.choice([f for f in os.listdir(videoCollection) if not f.startswith('.') and f.endswith('.mov')])
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollectionShorts/" + filename
    videoPath=videoCollection
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited_shorts.mp3")
    backgroundMusic = AudioFileClip("./assets/backgroundMusic/it-is-happy-main-9622.mp3")
    new_audioclip = originalVoiceOver
    comments = []
    with open(redditFolder + "/sync/screenshotTimestamps_shorts.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        check_idx = 0
        for timestamp in timestamps:
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                # check duration and only grab ones below 40 second to have short form
                if duration < 20:
                    comment = ImageClip(redditFolder + "/screenshots_shorts/" + timestamp["Filename"]).set_start(start).set_duration(duration).set_pos(("center","center"))
                    if comment.size[1] > backgroundVideoSize[1]:
                        resizeComment = comment.resize((int(backgroundVideoSize[0] * 0.8), int(backgroundVideoSize[1])*0.95))
                    else:
                        resizeComment = comment.resize(width=int(backgroundVideoSize[0] * 0.9))
                    comments.append([resizeComment, start + duration])
                    check_idx += 1
        pause = 2
        actual_length = new_audioclip.duration
        while actual_length > desired_duration:
            comments = comments[:-1]
            actual_length = comments[-1][1]
        new_audioclip = new_audioclip.subclip(0, actual_length + 0.5)
        new_backgroundAudio = backgroundMusic.set_duration(new_audioclip.duration)
        total_audio = CompositeAudioClip([new_backgroundAudio.volumex(0.02).set_start(0), new_audioclip.volumex(1.3).set_start(0)])
        cliped_duration = new_audioclip.duration
        loopedVideo = backgroundVideo.loop(duration=cliped_duration + pause)
        only_comments = [x[0]  for x in comments]
        final = CompositeVideoClip([loopedVideo, *only_comments])
        # final = CompositeVideoClip([*comments])
        # all audio
        ######################################
        # final.audio = new_audioclip
        final.audio = total_audio
        # final.set_audio(new_audioclip)
        ######################################
        # final = final.resize(0.3)
        # final = final.fx(vfx.speedx, speed)
        # string1 = "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
        # final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_shorts.mp4", ffmpeg_params = ["-filter_complex", str(string1), "-map", "[v]", "-map", "[a]"])
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_shorts_inter.mp4")
