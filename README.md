# Reddit


## Directory Structure

## Metadata format

## Instruction on pipleing of TTS
1) run newYTFolder.sh to create folder structure
2) change default screenshot location to make it eeasier for apple is
    'defaults write com.apple.screencapture location ./'
2) add reddit stories in ssml.xml located in reddit_yt_/ssml/original
3) add --alls creen shots for each comment in screenshots
3) run runRedditTTS.sh
4) wait few minutes for s3 to upload( this can be converted to lambda function that automatiicaly triggers later)
5) run voiceOverEdits.sh
note you cant run video ediditng on ubunut -- only on your mac!

## To backup all the speach marks and new TTS file
1) run in aws cli
    `aws s3 sync ./TTSData s3://reddityoutube2/`





