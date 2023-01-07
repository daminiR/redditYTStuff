from moviepy.editor import VideoFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.video.fx.speedx import speedx
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.audio.AudioClip import concatenate_audioclips
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
from pydub import AudioSegment
import os, random
import json

def createVideo(redditFolder, desired_length):
    desired_length = int(desired_length * 60) # 13 ish min
    # choose random video from collection
    metaDataDict = json.load(open(os.path.join(redditFolder, 'metadata.json'), "r"))
    filename = metaDataDict['videoFileUsed']
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollection/"
    videoPath=os.path.join(videoCollection, filename)
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    titleVideo = VideoFileClip(redditFolder + "/assets/titleVideo/title_video.mp4").resize(backgroundVideoSize)
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited.mp3")
    backgroundMusic = AudioFileClip("./assets/backgroundMusicLong/space-atmospheric-background-124841.mp3")
    subscribe_auido = AudioFileClip("assets/subscibeAudio/speech_20221107043941369.mp3")
    new_audioclip = originalVoiceOver.set_end(originalVoiceOver.duration - 0.30)
    sub_clip = VideoFileClip("assets/subscribeAnimation/reddit_subscribe2.mp4")
    offset_video = 0
    if "TwoSentenceHorror" in redditFolder:
        twoSentenceHorrorStartClip = VideoFileClip("assets/twoSentenceHorrorStart.mp4").resize(backgroundVideoSize)
        offset_video = twoSentenceHorrorStartClip.duration
    comments = []
    actual_length = False
    with open(redditFolder + "/sync/screenshotTimestamps.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        untilTitle = int(timestamps[1]["Time"] / 1000)
        if titleVideo.duration > untilTitle:
            # slow down title video to fit the length
            titleVideo = titleVideo.fx(speedx, 0.5)
        check_idx = 0
        for timestamp in timestamps:
            if "STORY" in timestamp["Mark Sentence"]:
                ## dont start new story if more than 20 minutes
                if timestamp["Time"] / 1000 > desired_length:
                    actual_length = timestamp["Time"] / 1000
                    break
                start = timestamp["Time"] / 1000 + offset_video
                duration = timestamp["Duration"] / 1000
                story_number = str(int(timestamp["Mark Sentence"].split("STORY")[1]) + 1)
                txt_clip = TextClip("Thread" +  " " + story_number, fontsize=75, font="Amiri-bold", color='white', bg_color='gray', stroke_color='black',stroke_width=2.5).set_start(start).set_duration(duration).set_pos("center")
                comments.append(txt_clip)
                txt_clip.close()
            else:
                start = timestamp["Time"] / 1000 + offset_video
                duration = timestamp["Duration"] / 1000
                comment = ImageClip(redditFolder + "/screenshots/" + timestamp["Filename"]).set_start(start).set_duration(duration).set_pos(("center","center"))
                if comment.size[1] > backgroundVideoSize[1]:
                    resizeComment = comment.resize((int(backgroundVideoSize[0] * 0.8), int(backgroundVideoSize[1])*0.95))
                else:
                    resizeComment = comment.resize(width=int(backgroundVideoSize[0] * 0.8))
                comments.append(resizeComment)

                resizeComment.close()
                comment.close()
            check_idx += 1
        pause = 1.5
        if actual_length == False:
            new_audioclip = new_audioclip
        else:
            new_audioclip = new_audioclip.subclip(0, actual_length)
        cliped_duration = new_audioclip.duration + offset_video
        if "TwoSentenceHorror" in redditFolder:
            title_comment = comments[0].set_duration(comments[0].duration).set_start(twoSentenceHorrorStartClip.duration)
        else:
            title_comment = comments[0]
        last_comment = comments[-1].set_duration(comments[-1].duration + 1)
        intermediate_comments = comments[1:-1]
        intermediate_comments.append(last_comment)
        new_comments = [title_comment]
        new_comments.extend(intermediate_comments)
        comments = new_comments
        # all video stuff
        ######################################
        final_sub_clip = sub_clip.set_start(cliped_duration + pause).set_pos(("center", "center")).resize(backgroundVideoSize).set_duration(sub_clip.duration)
        comments.append(final_sub_clip)
        if "TwoSentenceHorror" in redditFolder:
            loopedVideo = backgroundVideo.loop(duration=cliped_duration + pause - twoSentenceHorrorStartClip.duration)
            start_title = twoSentenceHorrorStartClip.duration
            titleclip = titleVideo.subclip(0, untilTitle).set_start(start_title)
            finalBackround = concatenate_videoclips([twoSentenceHorrorStartClip, titleclip, loopedVideo], method='chain')
            # twoSentenceHorrorStartClip.close()
        else:
            loopedVideo = backgroundVideo.loop(duration=cliped_duration + pause)
            titleclip = titleVideo.subclip(0, untilTitle)
            finalBackround = concatenate_videoclips([titleclip, loopedVideo], method='chain' )
        final = CompositeVideoClip([finalBackround, *comments])
        # final = CompositeVideoClip([finalBackround, comments[0]])
        # final = CompositeVideoClip([*comments])
        # all audio
        ######################################
        ## ad background music to speaking audio
        new_audioclip = CompositeAudioClip([backgroundMusic.volumex(0.03).set_duration(new_audioclip.duration).set_start(0), new_audioclip.set_start(0)])
        # new_audioclip =
        subscribe_total = CompositeAudioClip([sub_clip.audio.volumex(0.1).set_start(pause), subscribe_auido.set_start(pause)])
        if "TwoSentenceHorror" in redditFolder:
            finalAudio = concatenate_audioclips([twoSentenceHorrorStartClip.audio, new_audioclip, subscribe_total])
        else:
            finalAudio = concatenate_audioclips([new_audioclip, subscribe_total])
        final.audio = finalAudio
        ######################################
        # final = final.resize(0.01)
        # final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video.mp4",codec='hevc_videotoolbox', fps=24)
        # close all clips before wiritng
        #######################################
        # backgroundVideo.close()
        titleVideo.close()
        # originalVoiceOver.close()
        # subscribe_auido.close()
        # sub_clip.close()
        #######################################
        final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_video.mp4", threads=16, preset='ultrafast')
