# Reddit


## update to shorts first you need to sort by top and only have depth 1 for top comment. This is more intuitive.
## add this to the end of the url WHEN DOING SHORTS
?sort=top&depth=1
add limit=100
to limit to 100 comment or how many would approx 10-15 minutes no more than that to save aws polly cost
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
function removeRedBoundary() {
    const items = document.querySelectorAll("._3VH2iGVh92XtlKq0-eVoEN");
    for (let item of items) {
         item.remove();
    }
}

to remoe the red boundry gradient



3) run the function removeGradient()
and then can create exrto to pdf

## New Instruction on pipleing of TTS
1. add the diferrent reddit new folder titles in rootfolder in input.json
2. bash step_1.sh will create thos folders
3. for each website for reddit add the folowing jquery code to web inspect
    1.
function removeGradient() {
    const items = document.querySelectorAll(".TmlaIdEplCzZ0F1aRGYQh");
    const items_comminute_bar = document.querySelectorAll("._3Kd8DQpBIbsr5E1JcrMFTY._1tvThPWQpORoc2taKebHxs");
    const items_archive = document.querySelectorAll("._1EjIqPTCvhReSe3IjZptiB._1DUKbp8va6vxOv9zemBDBi");
    for (let item of items) {
         item.remove();
    }
    for (let item of items_comminute_bar) {
         item.remove();
    }
    for (let item of items_archive) {
         item.remove();
    }
    const comment_deleted_by_user = document.querySelectorAll("._3sf33-9rVAO_v4y0pIW_CH");
    for (let item of comment_deleted_by_user) {
         item.remove();
    }
    const top1 = document.querySelector("._2vkeRJojnV7cb9pMlPHy7d ")
    top1?.remove();
    const top2 = document.querySelector("._2L5G9B5yaoqW3IegiYN-FL")
    top2?.remove();
    const top3 = document.querySelector("._1gVVmSnHZpkUgVShsn7-ua")
    top3?.remove();

    const remove_by_mod = document.querySelector("._3sf33-9rVAO_v4y0pIW_CH")
    remove_by_mod?.remove();
    const blocked = document.querySelector(".jf95ZrrjIs2i--Ud8Kvb7._1DUKbp8va6vxOv9zemBDBi")
    blocked?.remove();
    const mod_comment = document.querySelector(".LWgI-A6rN9Wajn1VLxu2A._3AgEmWP1qkCB8nds7LhzEB")
    mod_comment?.parentElement.parentElement.parentElement.parentElement.remove()
    const upvotes = document.querySelector("._23h0-EcaBUorIHC-JZyh6J")
    upvotes?.remove();
    const title_posted = document.querySelector("._14-YvdFiW5iVvfe5wdgmET")
    title_posted?.remove();
    const title_chip = document.querySelector("._2fiIRtMpITeCAzXc4cANKp._1mK-LVHGTTlcFpMsjItjYJ")
    title_chip?.remove();
    const post_edits = document.querySelector("._1hwEKkB_38tIoal6fcdrt9")
    post_edits?.remove();
    const reply_block = document.querySelector("._1r4smTyOEZFO91uFIdWW6T.aUM8DQ_Nz5wL0EJc_wte6")
    reply_block?.remove();
    const suggested_block = document.querySelector("._2ulKn_zs7Y3LWsOqoFLHPo")
    suggested_block?.remove();
    const add_block = document.querySelector(".Pbz3gpOA6rvqdYoX_pOjn")
    add_block?.remove();
    const cont_block = document.querySelectorAll("._3ndawrYzcvjHPJFYUHijfP ")
    for (let item of cont_block) {
    item.remove();
    }
    const reply_block2 = document.querySelectorAll("._2HYsucNpMdUpYlGBMviq8M._23013peWUhznY89KuYPZKv")
    for (let item of reply_block2) {
    item.remove();
    }
    const awards = document.querySelectorAll(".n08B7PrU01wzgZYIh-s7N")
    for (let item of awards) {
    item.remove();
    }
    const red_shadow = document.querySelectorAll("._3VH2iGVh92XtlKq0-eVoEN")
    for (let item of red_shadow) {
    item.remove();
    }
    const chips = document.querySelectorAll("._3w527zTLhXkd08MyacMV9H")
    for (let item of chips) {
    item.remove();
    }
    const comment_button = document.querySelectorAll(".cmR5BF4NpBUm3DBMZCmJS._1cubpGNEaCAVnpJl1KBPcO._2q-ZKRaT1WjKg092R6La5J")
    for (let item of comment_button) {
    item.remove();
    }
    const in_comment_reply = document.querySelectorAll("._28lDeogZhLGXvE95QRPeDL")
    for (let item of in_comment_reply) {
    item.remove();
    }
    const gif_award = document.querySelectorAll("._15G4fCS1bzGgGK9kBOtN2t._28x1bnTjOY6zWZfooCxkKQ")
    for (let item of gif_award) {
    item.remove();
    }
    var header = document.getElementsByTagName('header')[0];
    header?.remove();
}
4. in the new folders created add the pdf exported from safary to each  ssml/edited as "reddit.pdf"
5. now run bash step_2.sh to create single pdf from pages in reddit.pdf  and TTS
6. wait a bit to let aws load file
7. run bash step_3.sh to get TTS and ready for creating video
8. now add the follwing by finding on pexels or pixabay
    1. title video in asset/titleVideo names as  title_video.mp4
    2. background video in asset/backgroundVideo names as  background_video.mp4
    3. thumnail image in assets/thumbnail_input_image/ as image.jpg
9. run bash step_4.sh to geenrate video and its thumbnail, NOTe this takes an hour per video

