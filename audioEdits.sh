#!/bin/bash
rootFolderString=$(jq .rootFolder inputs.json)
rootFolder=$(sed -e 's/^"//' -e 's/"$//' <<<"$rootFolderString")
subReddit=$(jq .subReddit inputs.json)
titleVideoFileString=$(jq .titleVideoFile inputs.json)
titleVideoFile=$(sed -e 's/^"//' -e 's/"$//' <<<"$titleVideoFileString")
backgroundVideoFileString=$(jq .backgroundVideoFile inputs.json)
backgroundVideoFile=$(sed -e 's/^"//' -e 's/"$//' <<<"$backgroundVideoFileString")

totalYTs=$(($(find ./${rootFolder} -maxdepth 1 -type d | wc -l) - 1))
redditFolder="${rootFolder}reddit_yt_${totalYTs}"
timestamps=$redditFolder"/sync/screenshotTimestamps.json"
originalVoiceOverFile=$redditFolder"/voiceOver/edited/eddited.mp3"
titleVideo=$redditFolder/assets/titleVideo/$titleVideoFile
backgroundVideo=$redditFolder/assets/backgroundVideo/$backgroundVideoFile


echo $originalVoiceOverFile
echo $backgroundVideo
ffmpeg  -hwaccel cuda -stream_loop -1 -i "$backgroundVideo" -i $originalVoiceOverFile -shortest -map 0:v:0 -map 1:a:0 -y ./out.mp4


#jq -c '.[][]' $timestamps | while read -r voiceMarks; do
#mark=$( echo $voiceMarks | jq '."Mark Sentence"' )
#if [[ $mark != *"STORY"* ]]; then
        #start=$( echo $voiceMarks | jq '."Time"' )
        #duration=$( echo $voiceMarks | jq '."Duration"' )
        #else
        #echo $mark
        #start=$( echo $voiceMarks | jq '."Time"' )
        #duration=$( echo $voiceMarks | jq '."Duration"' )
        ## whateevr works for now - very messy code
        ## TODO: fix
        #IFS='Y' read -ra stringStory <<< "$mark"
        #story_number=${stringStory[1]}
        #echo $story_number
#fi
#done


#ffmpeg -i video -i image1 -i image2 -i image3
 #-filter_complex
    #"[0][1]overlay=x=X:y=Y:enable='between(t,23,27)'[v1];
     #[v1][2]overlay=x=X:y=Y:enable='between(t,44,61)'[v2];
     #[v2][3]overlay=x=X:y=Y:enable='gt(t,112)'[v3]"
#-map "[v3]" -map 0:a  out.mp4


