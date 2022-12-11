"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json
import os
import sys

def getAWSTTSFiles(redditFolder, videoType):
    s3 = boto3.client('s3')
    if videoType == "long":
        mp3LogFile = 'mp3_log.json'
        maskLogFile = 'marks_log.json'
    else:
        mp3LogFile = 'mp3_log_shorts.json'
        maskLogFile = 'marks_log_shorts.json'
    mp3Log = open(redditFolder + '/logs/voiceOver/' + mp3LogFile, 'r')
    maskLog = open(redditFolder + '/logs/marks/' + maskLogFile, 'r')
    mp3Dict = json.load(mp3Log)
    maskDict = json.load(maskLog)
    try:
        TaskId_mp3=mp3Dict["SynthesisTask"]["TaskId"]
        TaskId_mask=maskDict["SynthesisTask"]["TaskId"]
        print(TaskId_mask)
        if videoType == "long":
            download_original = "original.mp3"
            download_marks ="marks.json"
        else:
            download_original = "original_shorts.mp3"
            download_marks ="marks_shorts.json"
        s3.download_file('reddityoutube2',  TaskId_mp3 + '.mp3', redditFolder + '/' + 'voiceOver/original/' + download_original)
        s3.download_file('reddityoutube2',  TaskId_mask + '.marks', redditFolder + '/' + 'marks/original/' + download_marks)

    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

