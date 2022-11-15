from moviepy.editor import *
from moviepy.video import *
from moviepy.audio import *
from moviepy.video.fx.resize import resize
from pydub import AudioSegment
import json

def createVideo(redditFolder, backgroundVideoFile, titleVideoFile):
    titleVideo = VideoFileClip(redditFolder + "/assets/titleVideo/" + titleVideoFile)
    backgroundVideo = VideoFileClip(redditFolder + "/assets/backgroundVideo/" + backgroundVideoFile)
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited.mp3")
    subscribe_auido = AudioFileClip("assets/subscibeAudio/speech_20221107043941369.mp3")

    subs_dur= subscribe_auido.duration
    new_audioclip = originalVoiceOver
    subscribe_clip = subscribe_auido
    tts_audio_length = new_audioclip.duration
    backgroundVideoSize = backgroundVideo.size

    sub_clip = VideoFileClip("assets/subscribeAnimation/reddit_subscribe2.mp4")
    blackBackground = ImageClip("assets/Screen Shot 2022-11-07 at 2.27.25 AM.png").set_duration(sub_clip.duration)
    final_sub_clip = sub_clip.set_start(tts_audio_length).set_pos(("center", "center")).resize(backgroundVideoSize).set_duration(sub_clip.duration)
    subscribe_total = CompositeAudioClip([sub_clip.audio.volumex(0.1), subscribe_auido])
    finalAudio = concatenate_audioclips([new_audioclip, subscribe_total])
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

        untilTitle = int(timestamps[2]["Time"] / 1000)
        if titleVideo.duration > untilTitle:
            titleclip = titleVideo.subclip(0, untilTitle)

        comments.append(final_sub_clip)
        finalBackround = concatenate_videoclips([titleclip, loopedVideo])
        final = CompositeVideoClip([finalBackround, *comments])
        final.audio = finalAudio
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video_trial.mp4", threads=4)
