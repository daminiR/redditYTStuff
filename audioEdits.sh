#!/bin/bash

rootFolderString=$(jq .rootFolder inputs.json)
rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$rootFolderString")
totalYTs=$(($(find $rootFolder -maxdepth 1 -type d | wc -l) - 1))
redditFolder="${rootFolder}/reddit_yt_${totalYTs}"
echo $redditFolder"/voiceOver/edited/edited.mp3"
timestamps=$redditFolder"/sync/screenshotTimestamps.json"
echo $timestamps

jq -c '.[][0]' $timestamps | while read voiceMark; do
    echo $voiceMark
    #if [ "$timestamps" == "tux" ]; then
done

