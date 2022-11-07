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
    subscribe_auido = AudioFileClip("assets/subscibeAudio/speech_20221107043941369.mp3")
    subs_dur= subscribe_auido.duration
    new_audioclip = CompositeAudioClip([originalVoiceOver])
    subscribe_clip = CompositeAudioClip([subscribe_auido])
    tts_audio_length = new_audioclip.duration
    blackBackground = ImageClip("assets/Screen Shot 2022-11-07 at 2.27.25 AM.png")
    backgroundVideoSize = backgroundVideo.size
    final_sub_clip = VideoFileClip("assets/subscribeAnimation/reddit_subscribe.mp4").set_start(tts_audio_length + 1).set_pos(("center", "center")).resize(backgroundVideoSize)

    finalAudio = concatenate_audioclips([new_audioclip, subscribe_clip])
    end = finalAudio.duration
    loopedVideo = backgroundVideo.loop(duration=tts_audio_length)
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

        comments.append(final_sub_clip)
        finalBackround = concatenate_videoclips([titleclip, loopedVideo, final_sub_clip])
        final = CompositeVideoClip([finalBackround, *comments])
        final.audio = finalAudio
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video.mp4")
