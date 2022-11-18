# Reddit


## Directory Structure

## Metadata format

## Instruction on pipleing of TTS
1) run step_1.sh to create folder structure
### on IOS
2) change default screenshot location to make it eeasier for apple is
    'defaults write com.apple.screencapture location ./'
### on Linux
So linux has some screenshot problems, the way to configure is following:
    1) first got to https://ubuntuhandbook.org/index.php/2022/04/get-back-gnome-screenshot-ubuntu-2204/ and foolow to setup
    2) then us gsettings set org.gnome.gnome-screenshot auto-save-directory /home/damini/redditYTStuff/TTSData/ytData/AskReddit/reddit_yt_3/screenshots/
    to set up location to save screens
2) add reddit stories in ssml.xml located in reddit_yt_{}/ssml/original
3) add --alls sreenshots for each comment in reddit_yt_{}/screenshots/ folder
3) run step_2.sh
4) wait few minutes for s3 to upload( this can be converted to lambda function that automatiicaly triggers later)
5) run step_3.sh
6) step__4.py
NOTE you cant run video editing on ubunutu -- only on your mac!
7) run ONLY ON MAC step_5.sh. Do Not run on ubunut
8) edit, metadata to add words you want to highlight e.i create a list of all the words
example:
{
"RedditTitle": "Reddit, what's your most \"I'm with the Boomers on this\" opinion?",
"highlights":  ["most", "with", "Boomers", "opinion"]
}
9) add single image for thumbnail image in reddit_yt_{}/assets/thumbnail_input_image renamed to thumnail.jpg
10) add fontSize for thumbnail title in inputs.json --> choose variable size and adjust to length of title
9) run step_6.sh for automatic thumbnail!

## To backup all the speach marks and new TTS file TO AWS
1) run in aws cli
    `aws s3 sync ./TTSData s3://reddityoutube2/`
## To backup all the speach marks and new TTS file FROM AWS to local
1) run in aws cli
    `aws s3 sync s3://reddityoutube2/ytData ./TTSData/ytData/ `

#Tip

try to edit everything on linux except image processing of step 6



#Notes for remoe gradient from reddit website to all proper pdf
1) open inspect element in reddit ask reddit whateever website to convert to pdf
2) paste this as a function in the conolse

function removeGradient() {
    const items = document.querySelectorAll(".TmlaIdEplCzZ0F1aRGYQh");
    for (let item of items) {
         item.remove();
    }
}
_3VH2iGVh92XtlKq0-eVoEN
function removeRedBoundary() {
    const items = document.querySelectorAll("._3VH2iGVh92XtlKq0-eVoEN");
    for (let item of items) {
         item.remove();
    }
}

to remoe the red boundry gradient



3) run the function removeGradient()
and then can create exrto to pdf

