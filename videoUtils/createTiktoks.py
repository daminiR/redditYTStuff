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

def createTiktoks(redditFolder, length, videoName):
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
    # backgroundMusic = AudioFileClip("./assets/backgroundMusic/space-atmospheric-background-124841.mp3")
    new_audioclip = originalVoiceOver
    tiktoks = []
    comments = []
    length = length
    length_idx = 1
    with open(redditFolder + "/sync/screenshotTimestamps_tiktok.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        check_idx = 0
        start_tiktok = 0
        all_comments = []
        offset = 0
        title = None
        for timestamp in timestamps[:-1]:
                start = timestamp["Time"] / 1000
                duration = timestamp["Duration"] / 1000
                if title == None:
                    comment = ImageClip(redditFolder + "/screenshots_tiktok/" + timestamp["Filename"])\
                    .set_start(start - offset).set_duration(duration).set_pos(("center","center"))
                else:
                    if length_idx == 1:
                        comment = ImageClip(redditFolder + "/screenshots_tiktok/" + timestamp["Filename"])\
                        .set_start(start - offset).set_duration(duration).set_pos(("center","center"))
                    else:
                        comment = ImageClip(redditFolder + "/screenshots_tiktok/" + timestamp["Filename"])\
                        .set_start(start - offset + title[0].duration + 1).set_duration(duration).set_pos(("center","center"))
                if comment.size[1] > backgroundVideoSize[1]:
                    resizeComment = comment.resize((int(backgroundVideoSize[0] * 0.8), int(backgroundVideoSize[1])*0.95))
                else:
                    resizeComment = comment.resize(width=int(backgroundVideoSize[0] * 0.9))
                if timestamp["Mark Sentence"] == "TITLE":
                    resizeComment.set_duration(duration + 1)
                    title = [resizeComment, start, start + duration + 1]
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
            if idx != 0:
                titleAudioClip = new_audioclip.subclip(title[1],  title[2])
                tiktokAudioClip = new_audioclip.subclip(tiktok[1] + 1,  tiktok[2])
                tiktokVideoClip = tiktok[0]
                finalAudio = concatenate_audioclips([titleAudioClip, tiktokAudioClip])
                # new_backgroundAudio = backgroundMusic.set_duration(finalAudio.duration)
                # total_audio = CompositeAudioClip([new_backgroundAudio.volumex(0.01), finalAudio.volumex(1.3)])
                loopedVideo = backgroundVideo.loop(duration=finalAudio.duration)
                tiktokVideoClip = [x[0].set_pos("center", "center")  for x in tiktokVideoClip]
                tiktokVideoClip.append(title[0])
                final2 = CompositeVideoClip([loopedVideo, *tiktokVideoClip])
                final2.audio = finalAudio
                if videoName == "shorts":
                    final2.write_videofile(redditFolder + "/youtubeVideo/" + "Part " + str(idx + 1) + ".mp4", fps= 24)
                else:
                    final2.write_videofile(redditFolder + "/youtubeVideo/" + "Part " + str(idx + 1) + " tiktok" + ".mp4", fps= 24)
            else:
                tiktokAudioClip = new_audioclip.subclip(tiktok[1] + 1,  tiktok[2])
                tiktokVideoClip = tiktok[0]
                finalAudio = concatenate_audioclips([tiktokAudioClip])
                # new_backgroundAudio = backgroundMusic.set_duration(finalAudio.duration)
                # total_audio = CompositeAudioClip([new_backgroundAudio.volumex(0.01), finalAudio.volumex(1.3)])
                loopedVideo = backgroundVideo.loop(duration=finalAudio.duration)
                tiktokVideoClip = [x[0].set_pos("center", "center")  for x in tiktokVideoClip]
                # tiktokVideoClip.append(title[0])
                final2 = CompositeVideoClip([loopedVideo, *tiktokVideoClip])
                final2.audio = finalAudio
                if videoName == "shorts":
                    final2.write_videofile(redditFolder + "/youtubeVideo/" + "Part " + str(idx + 1) + ".mp4", fps= 24)
                else:
                    final2.write_videofile(redditFolder + "/youtubeVideo/" + "Part " + str(idx + 1) + " tiktok" + ".mp4", fps= 24)

