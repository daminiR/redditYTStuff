#!/bin/bash

rootFolder="OCt_30_2022"
totalYTs=$(($(find ./OCt_30_2022 -maxdepth 1 -type d | wc -l) - 1 + 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
mkdir "${rootFolder}/reddit_yt_${totalYTs}"
cd "${rootFolder}/reddit_yt_${totalYTs}"
mkdir logs marks ssml voiceOver
cd logs
mkdir marks voiceOver
cd ../marks
mkdir edited original
cd ../ssml
mkdir edited original
cd ../voiceOver
mkdir edited original
cd ../
touch metadata.json

# now add ssml.xml file with template
cd ssml/original
touch ssml.xml
cd ../../../../
python3  ./editing/preXMl.py $redditFolder




