#!/bin/bash

rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
echo "Enter the video (youtube or tiktok): "
read videoType
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    mkdir $redditFolder
    cd $redditFolder
    if [ "$videoType" == "youtube" ]; then
        mkdir logs marks ssml voiceOver screenShotIds screenshots screenshots_shorts sync youtubeVideo assets pdf
    elif [ "$videoType" == "tiktok" ]; then
        mkdir logs marks ssml voiceOver screenShotIds screenshots_tiktok sync youtubeVideo assets pdf
    fi
    cd logs
    mkdir marks voiceOver
    cd ../marks
    mkdir edited original
    cd ../ssml
    mkdir edited
    cd ../voiceOver
    mkdir edited original
    cd ../
    touch metadata.json
    cd assets/
    mkdir titleVideo thumbnail_input_image
    cd ../
    cd sync
    mkdir errors
    # now add ssml.xml file with template
    cd ../../../../../
    python3  ./editing/preXMl.py $redditFolder
done





