#!/bin/bash
echo "Enter the video type: "
read videoType
#if [ "$videoType" = "short" ]; then
    #echo "Enter speed of short: "
    #read shortSpeed
#fi
shortSpeed=1.5
length_inputs=$(jq '.Inputs| length' inputs.json)
rootFolderString=( $(jq .Inputs[].rootFolder inputs.json) )

for var_idx in  $(seq $length_inputs);
do
    redditFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"${rootFolderString[var_idx - 1]}")
    echo $redditFolder
    if [ "$videoType" = "short" ]; then
        echo "in shorts"
        python3 ./main/moviepy_processing.py $redditFolder $videoType $shortSpeed
        ffmpeg -i $redditFolder/youtubeVideo/yt_shorts_inter.mp4 \
            -filter_complex "[0:v]setpts=0.667*PTS[v];[0:a]atempo=$shortSpeed[a]" \
            -map "[v]" -map "[a]" $redditFolder/youtubeVideo/yt_shorts.mp4
    else
        python3 ./main/moviepy_processing.py $redditFolder $videoType
    fi
    python3 ./main/moviepy_processing.py $redditFolder $videoType
done
