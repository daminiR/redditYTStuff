#!/bin/bash

rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    mkdir $redditFolder
    cd $redditFolder
    mkdir logs marks ssml voiceOver screenShotIds screenshots screenshots_shorts sync youtubeVideo assets pdf
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
done





