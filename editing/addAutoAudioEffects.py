from pydub import AudioSegment
import json

def audioEdits(redditFolder):
    outFile = 'eddited.mp3'
    outMarksFile = 'marks_edited_with_bits.json'
    originalVoiceOver = AudioSegment.from_mp3(redditFolder +  "/voiceOver/original/original.mp3")
    commentEffect = AudioSegment.from_mp3("assets/comments/notification-sound-7062.mp3")
    storyEffect = AudioSegment.from_mp3("assets/story/whoosh-6316.mp3")
    print("audio delay:", commentEffect.duration_seconds)
    print("story delay:", storyEffect.duration_seconds)
    last = 0
    end =  originalVoiceOver.duration_seconds * 1000
    edditedVoiceOver = originalVoiceOver[0:400]
    metadataFile = redditFolder + "/metadata.json"
    first_sentence = 0
    metaDataDict = {}
    edditedMarks = []
    sumDelay = 0
    with open(redditFolder + "/marks/edited/marks_processed.json", "r") as f, open(redditFolder + "/marks/edited/" + outMarksFile, 'w+') as marksOutput:
        voiceOverMarks = json.load(f)
        for mark in voiceOverMarks:
            print("delayed by", sumDelay)
            if 'sentence' in mark['type'] and first_sentence==0:
                metaDataDict['RedditTitle'] = mark['value']
                handle = open(metadataFile, 'w')
                first_sentence=1
                json.dump(metaDataDict, handle)
                handle.close()
                newMark = mark
                newMark["time"]  += sumDelay

            elif 'STORY' in mark['value']:
                reddit_slice = originalVoiceOver[last: mark['time']]
                # insert sound effect
                bit = reddit_slice + storyEffect
                edditedVoiceOver= edditedVoiceOver + bit
                last = mark['time']

                newMark = mark
                newMark["time"]  += sumDelay

                sumDelay += storyEffect.duration_seconds * 1000

            elif 'COMMENT' in mark['value']:
                reddit_slice = originalVoiceOver[last: mark['time']]
                # insert sound effect
                bit = reddit_slice + commentEffect
                edditedVoiceOver= edditedVoiceOver + bit
                last = mark['time']

                newMark = mark
                newMark["time"]  += sumDelay

                sumDelay += commentEffect.duration_seconds * 1000
            else:
                newMark = mark
                newMark["time"]  += sumDelay

            edditedMarks.append(newMark)
        json.dump(edditedMarks, marksOutput, indent=4)

        edditedVoiceOver = edditedVoiceOver + originalVoiceOver[last : end]
        edditedVoiceOver.export(redditFolder + '/' + 'voiceOver/' + 'edited/' + outFile, format="mp3")








