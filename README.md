# Reddit


## Directory Structure

## Metadata format

## Instruction on pipleing of TTS
1) run newYTFolder.sh to create folder structure
### on IOS
2) change default screenshot location to make it eeasier for apple is
    'defaults write com.apple.screencapture location ./'
### on Linux
So linux has some screenshot problems, the way to configure is following:
    1) first got to https://ubuntuhandbook.org/index.php/2022/04/get-back-gnome-screenshot-ubuntu-2204/ and foolow to setup
    2) then us gsettings set org.gnome.gnome-screenshot auto-save-directory /home/damini/redditYTStuff/TTSData/ytData/AskReddit/reddit_yt_3/screenshots/
    to set up location to save screens
2) add reddit stories in ssml.xml located in reddit_yt_/ssml/original
3) add --alls sreenshots for each comment in screenshots
3) run runRedditTTS.sh
4) wait few minutes for s3 to upload( this can be converted to lambda function that automatiicaly triggers later)
5) run voiceOverEdits.sh
note you cant run video ediditng on ubunut -- only on your mac!

## To backup all the speach marks and new TTS file TO AWS
1) run in aws cli
    `aws s3 sync ./TTSData s3://reddityoutube2/`
## To backup all the speach marks and new TTS file FROM AWS to local
1) run in aws cli
    `aws s3 sync s3://reddityoutube2/ytData ./TTSData/ytData/ `

#Tip

try to edit everything on linux
and then running text to speach and image to text on your mac :)




