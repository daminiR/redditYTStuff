#!/bin/bash
echo "Enter the video type: "
read videoType
rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    echo $redditFolder
    python3 ./main/edits.py $redditFolder $videoType
done

