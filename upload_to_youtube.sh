#!/bin/bash

length_inputs=$(jq '.Inputs| length' inputs_subs.json)
rootFolderString=( $(jq .Inputs[].rootFolder inputs_subs.json) )
description="❤️ Like & Subscribe for Reddit videos posted Daily:
🔔 Hit the notification bell so you don't miss any stories!

#AskReddit #Reddit #RedditStories  r/askreddit ask reddit"

for var_idx in  $(seq $length_inputs);
do
    redditFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"${rootFolderString[var_idx - 1]}")
    redditYTFIle=$redditFolder/youtubeVideo/yt_video.mp4
    thumbnail=/Users/daminirijhwani/redditYTStuff/$redditFolder/youtubeVideo/thumbnail.jpg
    title=( "$(jq .RedditTitle $redditFolder/metadata.json)" )
    echo $redditFolder $title $thumbnail
    python3 ./main/youtube_upload.py \
    --file $redditYTFIle \
    --title "$title" \
    --description "$description" \
    --category="22" \
    --privacyStatus "private" \
    --description "$description" \
    --thumbnailFile "$thumbnail"
    break
done
