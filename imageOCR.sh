#!/bin/bash

rootFolder="TTSData/ytData"
totalYTs=$(($(find ./${rootFolder} -maxdepth 1 -type d | wc -l) - 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
echo $redditFolder
python3 getIDs.py $redditFolder
