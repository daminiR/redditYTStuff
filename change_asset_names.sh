#!/bin/bash

rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    cd $redditFolder
    cd assets
    cd thumbnail_input_image
    mv * image.jpg
    cd ..
    cd titleVideo
    mv * title_video.mp4
    cd ~/redditYTStuff/
done





