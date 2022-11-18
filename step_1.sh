#!/bin/bash

rootFolderString=$(jq .rootFolder inputs.json)
rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$rootFolderString")
totalYTs=$(($(find ./${rootFolder} -maxdepth 1 -type d | wc -l) - 1 + 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
mkdir "${rootFolder}/reddit_yt_${totalYTs}"
cd "${rootFolder}/reddit_yt_${totalYTs}"
mkdir logs marks ssml voiceOver screenShotIds screenshots sync youtubeVideo assets pdf
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
touch inputs.json
cd assets/
mkdir titleVideo backgroundVideo thumbnail_input_image
cd ../
cd sync
mkdir errors
cd ..

# now add ssml.xml file with template
cd ssml/original
touch ssml.xml
cd ../../../../../../
python3  ./editing/preXMl.py $redditFolder




