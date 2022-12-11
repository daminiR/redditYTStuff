#!/bin/bash
echo "Enter the video type: "
read videoType
rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    echo $redditFolder
    python3 ./main/createPDF.py $redditFolder $videoType
    #echo converting pdf to png....
    if [ "$videoType" == "short" ]; then
        echo "short video type"
        convert  -flatten -quality 50 -density 144  $redditFolder"/pdf/reddit_shorts_single_page.pdf" $redditFolder"/pdf/reddit_shorts.png"
        rm -r $redditFolder/screenshots_shorts/*
    else
        echo "long video type"
        convert  -flatten -quality 50 -density 144  $redditFolder"/pdf/reddit_single_page.pdf" $redditFolder"/pdf/reddit.png"
        rm -r $redditFolder/screenshots/*
    fi
    python3 ./main/createScreens.py $redditFolder $videoType
done




