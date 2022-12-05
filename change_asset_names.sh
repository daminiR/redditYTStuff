#!/bin/bash

rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    cd $redditFolder
    cd pdf
    mv * reddit.pdf
    cd ../
    #rm reddit.pdf

    #rm reddit.png
    #rm reddit_single_page.pdf

    #cd assets/backgroundVideo
    #mv * background_video.mp4
    cd assets/thumbnail_input_image
    mv * image.jpg
    cd ../titleVideo
    mv * title_video.mp4
    cd ~/redditYTStuff/
done





