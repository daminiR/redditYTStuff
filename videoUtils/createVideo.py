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

def createVideo(redditFolder):
    desired_length = 1200 # 20 sh min
    # choose random video from collection
    metaDataDict = json.load(open(os.path.join(redditFolder, 'metadata.json'), "r"))
    filename = metaDataDict['videoFileUsed']
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollection/"
    videoPath=os.path.join(videoCollection, filename)
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    titleVideo = VideoFileClip(redditFolder + "/assets/titleVideo/title_video.mp4").resize(backgroundVideoSize)
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited.mp3")
    subscribe_auido = AudioFileClip("assets/subscibeAudio/speech_20221107043941369.mp3")
    subs_dur= subscribe_auido.duration
    new_audioclip = originalVoiceOver
    tts_audio_length = new_audioclip.duration
    sub_clip = VideoFileClip("assets/subscribeAnimation/reddit_subscribe2.mp4")
    comments = []
    with open(redditFolder + "/sync/screenshotTimestamps.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        untilTitle = int(timestamps[1]["Time"] / 1000)
        if titleVideo.duration > untilTitle:
            # slow down title video to fit the length
            titleVideo = titleVideo.fx(vfx.speedx, 0.5)
        check_idx = 0
        for timestamp in timestamps:
            if "STORY" in timestamp["Mark Sentence"]:
                ## dont start new story if more than 20 minutes
                if timestamp["Time"] / 1000 > desired_length:
                    actual_length = timestamp["Time"] / 1000
                    break
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                story_number = timestamp["Mark Sentence"].split("STORY")[1]
                txt_clip = TextClip("STORY" +  " " + story_number, fontsize=75, font="Amiri-bold", color='white', bg_color='gray', stroke_color='black',stroke_width=2.5).set_start(start).set_duration(duration).set_pos("center")
                comments.append(txt_clip)
            else:
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                print(timestamp["Filename"])
                comment = ImageClip(redditFolder + "/screenshots/" + timestamp["Filename"]).set_start(start).set_duration(duration).set_pos(("center","center"))
                if comment.size[1] > backgroundVideoSize[1]:
                    resizeComment = comment.resize((int(backgroundVideoSize[0] * 0.8), int(backgroundVideoSize[1])*0.95))
                else:
                    resizeComment = comment.resize(width=int(backgroundVideoSize[0] * 0.8))
                comments.append(resizeComment)
            check_idx += 1

        # print(*comments, sep = "\n")
        # linger the last comment a bit longer!
        # all audo stuff
        pause = 2
        new_audioclip = new_audioclip.subclip(0, actual_length)
        cliped_duration = new_audioclip.duration
        # last_comment = comments[-1].set_duration(comments[-1].duration + 1.5)
        # comments = comments[:-1]
        # comments.append(last_comment)
        # all video stuff
        ######################################
        final_sub_clip = sub_clip.set_start(cliped_duration + pause).set_pos(("center", "center")).resize(backgroundVideoSize).set_duration(sub_clip.duration)
        comments.append(final_sub_clip)
        titleclip = titleVideo.subclip(0, untilTitle)
        loopedVideo = backgroundVideo.loop(duration=cliped_duration + pause)
        finalBackround = concatenate_videoclips([titleclip, loopedVideo])
        # final = CompositeVideoClip([finalBackround, *comments])
        final = CompositeVideoClip([*comments])
        # all audio
        ######################################
        subscribe_total = CompositeAudioClip([sub_clip.audio.volumex(0.1).set_start(pause), subscribe_auido.set_start(pause)])
        finalAudio = concatenate_audioclips([new_audioclip,  subscribe_total])
        final.audio = finalAudio
        ######################################
        final = final.resize(0.5)
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video.mp4")
