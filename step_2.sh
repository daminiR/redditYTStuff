#!/bin/bash
echo "Enter the video type: "
read videoType
rootFolderString=$(jq .Inputs[].rootFolder inputs.json)
for var in $rootFolderString
do
    rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$var")
    redditFolder=$rootFolder
    echo $redditFolder
    #python3 ./main/createPDF.py $redditFolder $videoType
    #echo converting pdf to png....
    if [ "$videoType" == "short" ]; then
        echo "short video type"
        convert  -flatten -quality 50 -density 144  $redditFolder"/pdf/reddit_shorts_single_page.pdf" $redditFolder"/pdf/reddit_shorts.png"
        rm -r $redditFolder/screenshots_shorts/*
    elif [ "$videoType" == "long" ]; then
        echo "long video type"
        convert  -flatten -quality 50 -density 144  $redditFolder"/pdf/reddit_single_page.pdf" $redditFolder"/pdf/reddit.png"
        rm -r $redditFolder/screenshots/*
    elif [ "$videoType" == "tiktok" ]; then
        echo "tiktok video type"
        #convert  -flatten -quality 50 -density 144  $redditFolder"/pdf/reddit_tiktok_single_page.pdf" $redditFolder"/pdf/reddit_tiktok.png"
        rm -r $redditFolder/screenshots_tiktok/*
    fi
    python3 ./main/createScreens.py $redditFolder $videoType
done




