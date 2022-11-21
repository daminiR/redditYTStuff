#!/bin/bash

rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    cd $redditFolder
    cd assets/backgroundVideo
    mv * background_video.mp4
    cd ../titleVideo
    mv * title_video.mp4
    cd ~/redditYTStuff/
done





