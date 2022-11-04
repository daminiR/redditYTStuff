from pydub import AudioSegment
import os
import json

def audioEdits(redditFolder):
    outFile = 'eddited.mp3'
    originalVoiceOver = AudioSegment.from_mp3(redditFolder +  "/voiceOver/original/original.mp3")
    commentEffect = AudioSegment.from_mp3("assets/comments/notification-sound-7062.mp3")
    storyEffect = AudioSegment.from_mp3("assets/story/whoosh-6316.mp3")
    last = 0
    end =  originalVoiceOver.duration_seconds * 1000
    edditedVoiceOver = originalVoiceOver[0:400]
    with open(redditFolder + "/marks/edited/marks_processed.json") as f:
        voiceOverMarks = json.load(f)
        for mark in voiceOverMarks:
            if 'STORY' in mark['value']:
                reddit_slice = originalVoiceOver[last: mark['time']]
                # insert sound effect
                bit = reddit_slice + storyEffect
                edditedVoiceOver= edditedVoiceOver + bit
                last = mark['time']
            if 'COMMENT' in mark['value']:
                reddit_slice = originalVoiceOver[last: mark['time']]
                # insert sound effect
                bit = reddit_slice + commentEffect
                edditedVoiceOver= edditedVoiceOver + bit
                last = mark['time']

        edditedVoiceOver = edditedVoiceOver + originalVoiceOver[last : end]
        edditedVoiceOver.export(redditFolder + '/' + 'voiceOver/' + 'edited/' + outFile, format="mp3")








