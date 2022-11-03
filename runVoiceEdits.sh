#!/bin/bash

rootFolder="OCt_30_2022"
totalYTs=$(($(find ./OCt_30_2022 -maxdepth 1 -type d | wc -l) - 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
echo $redditFolder
python3 edits.py $redditFolder
