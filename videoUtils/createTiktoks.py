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

def createTiktoks(redditFolder):
    speed = 1
    desired_duration = speed * 40
    # choose random video from collection
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollectionShorts/"
    filename = random.choice([f for f in os.listdir(videoCollection) if not f.startswith('.') and f.endswith('.mov')])
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollectionShorts/" + filename
    videoPath=videoCollection
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    originalVoiceOver = AudioFileClip(redditFolder +  "/voiceOver/edited/eddited_tiktok.mp3")
    backgroundMusic = AudioFileClip("./assets/backgroundMusic/it-is-happy-main-9622.mp3")
    new_audioclip = originalVoiceOver
    tiktoks = []
    comments = []
    length = 130
    length_idx = 1
    with open(redditFolder + "/sync/screenshotTimestamps_tiktok.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        check_idx = 0
        start_tiktok = 0
        all_comments = []
        offset = 0
        title = None
        for timestamp in timestamps:
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                if title == None:
                    comment = ImageClip(redditFolder + "/screenshots_tiktok/" + timestamp["Filename"])\
                    .set_start(start - offset).set_duration(duration).set_pos(("center","center"))
                else:
                    comment = ImageClip(redditFolder + "/screenshots_tiktok/" + timestamp["Filename"])\
                    .set_start(start - offset + title[0].duration).set_duration(duration).set_pos(("center","center"))
                if comment.size[1] > backgroundVideoSize[1]:
                    resizeComment = comment.resize((int(backgroundVideoSize[0] * 0.8), int(backgroundVideoSize[1])*0.95))
                else:
                    resizeComment = comment.resize(width=int(backgroundVideoSize[0] * 0.9))
                if timestamp["Mark Sentence"] == "TITLE":
                    resizeComment.set_duration(duration)
                    title = [resizeComment, start, + duration]
                else:
                    comments.append([resizeComment, start + duration])
                    all_comments.append([resizeComment, start + duration])
                check_idx += 1
                if start > length * length_idx:
                    length_idx += 1
                    end_tiktok = start + duration
                    total_comments = [title]
                    total_comments.extend(comments)
                    tiktoks.append((total_comments, start_tiktok, end_tiktok))
                    start_tiktok = end_tiktok
                    comments = [title]
                    offset =  end_tiktok
        for idx, tiktok in enumerate(tiktoks):
            titleAudioClip = new_audioclip.subclip(title[1],  title[2])
            tiktokAudioClip = new_audioclip.subclip(tiktok[1],  tiktok[2])
            tiktokVideoClip = tiktok[0]
            finalAudio = concatenate_audioclips([titleAudioClip, tiktokAudioClip])
            loopedVideo = backgroundVideo.loop(duration=finalAudio.duration)
            tiktokVideoClip = [x[0].set_pos("center", "center")  for x in tiktokVideoClip]
            tiktokVideoClip.append(title[0])
            final2 = CompositeVideoClip([loopedVideo, *tiktokVideoClip])
            final2.audio = finalAudio
            final2.write_videofile(redditFolder + "/youtubeVideo/" + "yt_tiktok_inter_" + str(idx + 1) + ".mp4", fps= 24)



            # if idx == 5:
                # break
            # titleAudioClip = new_audioclip.subclip(title[1],  title[2] + 1)
            # tiktokAudioClip = new_audioclip.subclip(tiktok[1],  tiktok[2] + 1)
            # titleVideoClip = CompositeVideoClip([title[0]])
            # # tiktokVideoClip = final.subclip(tiktok[1], tiktok[2] + 1)
            # tiktokVideoClip = tiktok[0]
            # finalAudio = concatenate_audioclips([titleAudioClip, tiktokAudioClip])
            # # finalVideo = concatenate_videoclips([titleVideoClip, final2])
            # # total_background = max(finalVideo.duration, finalAudio.duration)
            # loopedVideo = backgroundVideo.loop(duration=finalAudio.duration)
            # tiktokVideoClip = [x[0].set_pos("center", "center")  for x in tiktokVideoClip]
            # final2 = CompositeVideoClip([titleVideoClip, *tiktokVideoClip])

            # final2 = CompositeVideoClip([loopedVideo, final2])
            # final2.audio = finalAudio
            # final2.write_videofile(redditFolder + "/youtubeVideo/" + "yt_tiktok_inter_" + str(idx + 1) + ".mp4", fps= 24)
        # final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_shorts.mp4", ffmpeg_params = ["-filter_complex", str(string1), "-map", "[v]", "-map", "[a]"])

        # while actual_length > desired_duration:
            # comments = comments[:-1]
            # actual_length = comments[-1][1]
        # new_audioclip = new_audioclip.subclip(0, actual_length + 0.5)
        # new_backgroundAudio = backgroundMusic.set_duration(new_audioclip.duration)
        # total_audio = CompositeAudioClip([new_backgroundAudio.volumex(0.02).set_start(0), new_audioclip.volumex(1.3).set_start(0)])
        # cliped_duration = new_audioclip.duration
        # loopedVideo = backgroundVideo.loop(duration=cliped_duration + pause)
        # only_comments = [x[0]  for x in comments]
        # final = CompositeVideoClip([loopedVideo, *only_comments])
        # final = CompositeVideoClip([*comments])
        # all audio
        ######################################
        # final.audio = new_audioclip
        # final.audio = total_audio
        # final.set_audio(new_audioclip)
        ######################################
        # final = final.resize(0.3)
        # final = final.fx(vfx.speedx, speed)
        # string1 = "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"
        # final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_shorts.mp4", ffmpeg_params = ["-filter_complex", str(string1), "-map", "[v]", "-map", "[a]"])
        # final.write_videofile(redditFolder + "/youtubeVideo/" + "yt_shorts_inter.mp4")
