from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import json
import os
import sys
import subprocess
from tempfile import gettempdir

def TTS(redditFolder, videType='long'):
    session = Session(profile_name="default")
    polly = session.client("polly")
    dirRedditXML= redditFolder + "/ssml/edited"
    if videType =='long':
        redditFile = 'ssml_processed.xml'
    else:
        redditFile = 'ssml_processed_shorts.xml'
    with open(dirRedditXML + '/' + redditFile, 'r') as f:
        redditText = f.read()
        # first synthesis speech
        try:
            # Request speech synthesis
            if videType =='long':
                mp3Log = 'mp3_log.json'
            else:
                mp3Log = 'mp3_log_shorts.json'
            response = polly.start_speech_synthesis_task(
                Text=redditText,
                OutputFormat="mp3",
                TextType="ssml",
                OutputS3BucketName="reddityoutube2",
                VoiceId="Matthew",
                Engine="neural")
            json_obj = json.dumps(response, indent=4, default=str)
            with open(redditFolder + '/logs/voiceOver/' + mp3Log, 'w') as f:
                f.write(json_obj)

        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        try:
            # Request speech metadata
            if videType =='long':
                mp3Log = 'marks_log.json'
            else:
                mp3Log = 'marks_log_shorts.json'
            response = polly.start_speech_synthesis_task(
                Text=redditText,
                OutputFormat="json",
                TextType="ssml",
                OutputS3BucketName="reddityoutube2",
                SpeechMarkTypes=[
                    'ssml',
                    'sentence'
                ],
                VoiceId="Matthew",
                Engine="neural")
            json_obj = json.dumps(response, indent=4, default=str)
            with open(redditFolder + '/logs/marks/' + mp3Log, 'w') as f:
                f.write(json_obj)
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

