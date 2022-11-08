#!/bin/bash

rootFolderString=$(jq .rootFolder inputs.json)
rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$rootFolderString")
totalYTs=$(($(find ./${rootFolder} -maxdepth 1 -type d | wc -l) - 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
python3 main.py $redditFolder




