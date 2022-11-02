"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import json
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
def getAWSTTSFiles(root_dir):
    session = Session(profile_name="default")
    polly = session.client("polly")

    s3 = boto3.client('s3')

    dirRedditXML= '../OCt_30_2022/reddit_yt_2'
    mp3LogFile = 'mp3_log.json'
    maskLogFile = 'mask_log.json'
    mp3Log = open(dirRedditXML + '/' + mp3LogFile, 'r')
    maskLog = open(dirRedditXML + '/' + maskLogFile, 'r')
    mp3Dict = json.load(mp3Log)
    maskDict = json.load(maskLog)
# first synthesis speech
    try:
        # Request speech synthesis
        TaskId_mp3=mp3Dict["SynthesisTask"]["TaskId"]
        TaskId_mask=maskDict["SynthesisTask"]["TaskId"]
        print(TaskId_mask)
        s3.download_file('reddityoutube2', TaskId_mp3 + '.mp3', dirRedditXML + '/' + 'voiceOver/original/' + 'reddit_original.mp3')
        s3.download_file('reddityoutube2', TaskId_mask + '.marks', dirRedditXML + '/' + 'marks/' + 'reddit_mask.json')




    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

