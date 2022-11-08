#!/bin/bash

rootFolderString=$(jq .rootFolder inputs.json)
rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$rootFolderString")
subReddit=$(jq .subReddit inputs.json)
titleVideoFileString=$(jq .titleVideoFile inputs.json)
titleVideoFile=$(sed -e 's/^"//' -e 's/"$//' <<<"$titleVideoFileString")
echo $titleVideoFile
backgroundVideoFileString=$(jq .backgroundVideoFile inputs.json)
backgroundVideoFile=$(sed -e 's/^"//' -e 's/"$//' <<<"$backgroundVideoFileString")

echo $rootFolder
totalYTs=$(($(find $rootFolder -maxdepth 1 -type d | wc -l) - 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
python3 getIDs.py $redditFolder "${titleVideoFile}" "${backgroundVideoFile}"
