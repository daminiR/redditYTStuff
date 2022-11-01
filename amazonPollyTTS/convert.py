"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import json
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

dirRedditXML= '../OCt_30_2022/reddit_yt_2'
redditFile = 'reddit_1.xml_processed.xml'
with open(dirRedditXML + '/' + redditFile, 'r') as f:
    redditText = f.read()
    # first synthesis speech
    try:
        # Request speech synthesis
        mp3Log = 'mp3_log.json'
        response = polly.start_speech_synthesis_task(
            Text=redditText,
            OutputFormat="mp3",
            TextType="ssml",
            OutputS3BucketName="reddityoutube2",
            VoiceId="Matthew",
            Engine="neural")
        json_obj = json.dumps(response, indent=4, default=str)
        with open(dirRedditXML + '/' + mp3Log, 'w') as f:
            f.write(json_obj)

    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

    try:
        # Request speech metadata
        mp3Log = 'mask_log.json'
        response = polly.start_speech_synthesis_task(
            Text=redditText,
            OutputFormat="json",
            TextType="ssml",
            OutputS3BucketName="reddityoutube2",
            SpeechMarkTypes=[
                'ssml',
            ],
            VoiceId="Matthew",
            Engine="neural")
        json_obj = json.dumps(response, indent=4, default=str)
        with open(dirRedditXML + '/' + mp3Log, 'w') as f:
            f.write(json_obj)
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

# Access the audio stream from the response
    # if "AudioStream" in response:
        # # Note: Closing the stream is important because the service throttles on the
        # # number of parallel connections. Here we are using contextlib.closing to
        # # ensure the close method of the stream object will be called automatically
        # # at the end of the with statement's scope.
            # print("did we make it here")
            # with closing(response["AudioStream"]) as stream:
               # output = os.path.join("/home/damini/redditStuff/OCt_30_2022/reddit_yt_2/test", "speech.mp3")

               # try:
                # # Open a file for writing the output as a binary stream
                    # with open(output, "wb") as file:
                       # file.write(stream.read())
               # except IOError as error:
                  # # Could not write to file, exit gracefully
                  # print(error)
                  # sys.exit(-1)

    # else:
        # # The response didn't contain audio data, exit gracefully
        # print("Could not stream audio")
        # sys.exit(-1)

