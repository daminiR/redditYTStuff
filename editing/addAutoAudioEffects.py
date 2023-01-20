from pydub import AudioSegment
import json

def audioEdits(redditFolder, videoType='long'):
    if videoType == "long":
        outFile = 'eddited.mp3'
        outMarksFile = 'marks_edited_with_bits.json'
        originalVoiceOver = "original.mp3"
        processed_marks="marks_processed.json"
    elif videoType == "short":
        outFile = 'eddited_shorts.mp3'
        outMarksFile = 'marks_edited_with_bits_shorts.json'
        originalVoiceOver = "original_shorts.mp3"
        processed_marks="marks_processed_shorts.json"
    elif videoType == "tiktok":
        outFile = 'eddited_tiktok.mp3'
        outMarksFile = 'marks_edited_with_bits_tiktok.json'
        originalVoiceOver = "original_tiktok.mp3"
        processed_marks="marks_processed_tiktok.json"

    originalVoiceOver = AudioSegment.from_mp3(redditFolder +  "/voiceOver/original/" + originalVoiceOver)
    commentEffect = AudioSegment.from_mp3("assets/comments/comment_3.mp3")
    storyEffect = AudioSegment.from_mp3("assets/story/whoosh-6316.mp3")
    last = 0
    end =  originalVoiceOver.duration_seconds * 1000
    edditedVoiceOver = originalVoiceOver[0:400]
    if videoType=="long":
        metadataFile = redditFolder + "/metadata.json"
    first_sentence = 0
    edditedMarks = []
    sumDelay = 0
    with open(redditFolder + "/marks/edited/" + processed_marks, "r") as f, open(redditFolder + "/marks/edited/" + outMarksFile, 'w+') as marksOutput:
        voiceOverMarks = json.load(f)
        for idx, mark in enumerate(voiceOverMarks):
            if 'sentence' in mark['type'] and first_sentence==0:
                # y = {'RedditTitle' : mark['value']}
                if videoType == 'long':
                    y1 = {'highlights' : []}
                    handle = open(metadataFile, 'r')
                    oldMetaData = json.load(handle)
                    # oldMetaData.update(y)
                    oldMetaData.update(y1)
                    first_sentence=1
                    add = open(metadataFile, 'w')
                    json.dump(oldMetaData, add, indent=4)
                    handle.close()
                newMark = mark
                newMark["time"]  += sumDelay
            elif 'STORY' in mark['value']:
                reddit_slice = originalVoiceOver[last: mark['time']]
                bit = reddit_slice + storyEffect
                edditedVoiceOver= edditedVoiceOver + bit
                last = mark['time']
                newMark = mark
                newMark["time"]  += sumDelay
                sumDelay += storyEffect.duration_seconds * 1000
            elif 'COMMENT' in mark['value'] and 'END' not in mark['value'] and \
                'STORY' not in voiceOverMarks[idx - 1]['value'] \
                and first_sentence == 1:
                reddit_slice = originalVoiceOver[last: mark['time']]
                if videoType =='long':
                    bit = reddit_slice + commentEffect
                    edditedVoiceOver= edditedVoiceOver + bit
                    last = mark['time']
                    newMark = mark
                    newMark["time"]  += sumDelay
                    sumDelay += commentEffect.duration_seconds * 1000
                else:
                    bit = reddit_slice
                    edditedVoiceOver= edditedVoiceOver + bit
                    last = mark['time']
                    newMark = mark
                    newMark["time"]  += sumDelay
            else:
                newMark = mark
                newMark["time"]  += sumDelay
            edditedMarks.append(newMark)
        json.dump(edditedMarks, marksOutput, indent=4)

        edditedVoiceOver = edditedVoiceOver + originalVoiceOver[last : end]
        edditedVoiceOver.export(redditFolder + '/' + 'voiceOver/' + 'edited/' + outFile, format="mp3")








