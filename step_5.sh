#!/bin/bash
echo "Enter the video type: "
read videoType
if [ "$videoType" = "long" ]; then
    echo "Enter desired of length of video(min): "
    read desired_length
fi
shortSpeed=1.3
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
            -filter_complex "[0:v]setpts=0.769*PTS[v];[0:a]atempo=$shortSpeed[a]" \
            -map "[v]" -map "[a]" $redditFolder/youtubeVideo/yt_shorts.mp4
    elif [ "$videoType" = "long" ]; then
        python3 ./main/moviepy_processing.py $redditFolder $videoType $desired_length
    elif [ "$videoType" = "tiktok" ]; then
        python3 ./main/moviepy_processing.py $redditFolder $videoType
    fi
done
