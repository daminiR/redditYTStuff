import os
import fitz
import cv2
import json
import re
from moviepy.editor import VideoFileClip

def convertToBox(x1, y1, x2, y2):
    return [int((x2 + x1)/2 ), int((y2 + y1)/2), int(x2 - x1), int(y2 - y1)]

def redo():
    inputFile = "/Users/daminirijhwani/redditYTStuff/assets/abreviations.json"
    outFile = "/Users/daminirijhwani/redditYTStuff/assets/abreviations_new.json"
    with open(inputFile, 'r') as input, open(outFile, 'w+') as output:
        lines = input.readlines()
        for line in lines:
            line = re.sub('\"', ' \" ', line)
            output.write(line)

def cleanAbreviations(new):
    inputFile = "/Users/daminirijhwani/redditYTStuff/assets/abreviations_new.json"
    with open(inputFile, 'r') as h:
        lines = json.load(h)["abreviations"]
        for k, v in lines.items():
            new = new.replace(k, v)
            new = new.replace(k.upper(), v)
        return new

def redditAcronyms(line):
    new = line.replace("AITA", "Am I The Asshole")
    new = line.replace("AMA", "Ask Me Anything")
    new = new.replace("AMAA", " Ask Me Almost Anything")
    new = new.replace("DAE", "Does Anyone Else")
    new = new.replace("ELI5", "Explain like I'm 5")
    new = new.replace("FTA", "From The Article")
    new = new.replace("FTFY", "Fixed That For You")
    new = new.replace("GW", "Gone Wild")
    new = new.replace("IAMA", "I Am A")
    new = new.replace("IMO", "In My Opinion")
    new = new.replace("IMHO", "In My Humble (Honest) Opinion")
    new = new.replace("IIRC", "If I Recall Correctly")
    new = new.replace("ITT", "In This Thread")
    new = new.replace("MIC", "More In Comments")
    new = new.replace("OP", "O.P")
    new = new.replace("RTFA", "Read the fucking article")
    new = new.replace("SRD", "Subreddit drama")
    new = new.replace("TIL", "Today, I learned")
    new = new.replace("WIP", "Work in progress")
    new = new.replace("NTA", "Not the Asshole")
    new = new.replace("YTA", "You're the Asshole")
    new = new.replace("WIBTA", "Would I be the asshole")
    new = new.replace("NAH", "no assholes here")
    new = new.replace("ESH", "everyone sucks here")
    new = new.replace("WIBTA", "Would I be the asshole")
    new = new.replace("WTF", "W.T.F")
    new = new.replace("CMV", "Change my view")
    new = new.replace("IANAD", "I am not a doctor")
    new = new.replace("IANAL", "I am not a lawyer")
    new = new.replace("MRW", "My reaction when")
    new = new.replace("MFW", "My face when")
    new = new.replace("MFW", "Public service announcement")
    new = new.replace("YSK", "You should know")
    new = new.replace("TL;DR ", "Too long; Didn’t read")
    new = new.replace("OC", "O.C")
    new = new.replace("SRS", "Shit Reddit Says")
    new = new.replace("SO", "Significant Other")
    new = new.replace("DM;HS", "Doesnt Matter, Had Sex")
    new = new.replace("IRL", "In Real Life")
    new = new.replace("GTFO", "Get The Fuck Out")
    new = new.replace("YMMV", "your mileage may vary")
    new = new.replace("SMH", "Shaking my head")
    new = new.replace("LSHMSFOAIDMT", "Laughing So Hard My Sombrero Falls Off and I Drop My Taco")
    return new
def cleanTTS(line):
    gibrish = [
        "Posts\n",
        "Wiki\n",
        "Best of AskReddit\n",
        "r/AskReddit\n",
"Search Reddit\n",
"r/AskReddit ⌧\n",
"� Advertise\n",
        "Gilded\n",
        "Sort By: Best\n",
        "Related Subreddits\n",
        "Secret\n",
        "� Award\n",
        "� Share\n",
        "� Save\n",
        "This thread is archived\n",
        "New comments cannot be posted and votes cannot be cast\n",
        "�\n"
    ]
    regex_user= r'Comment deleted by user · \d{1,3} (days|mo.|yr.) ago(.*)'
    regex_hidden_user = r'· \d{1,3} (days|mo.|yr.) ago(.*)$'
    regex_comments=r'\d{1,5}.\dk'
    regex_more=r'\d{1, 4} More$'
    new = line.replace("\"", "")
    new = new.replace("&", "&amp;")
    new = new.replace("\'", "&apos;")
    new = new.replace("<", "&lt;")
    new = new.replace(">", "&gt;")
    if "hardlyHuman23" in new:
        new = ""
    for gib in gibrish:
        new = new.replace(gib, "")
    # regex stuff
    deleted_found = re.search(regex_user,new)
    if deleted_found:
        new = re.sub(regex_user,  "", new)
    if re.search(regex_comments,new):
        new = ""
    if re.search(regex_more,new):
        new = ""
    if re.search(regex_hidden_user,new):
        new = ""
    return new

def generateScreensSSML(rootDir):
    metaDataDict = json.load(open(os.path.join(rootDir, 'metadata.json'), "r"))
    filename = metaDataDict['videoFileUsed']
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollection/"
    videoPath=os.path.join(videoCollection, filename)
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    H = backgroundVideoSize[1]
    scale = 2
    file_path = rootDir + "/pdf/reddit_single_page.pdf"
    reddit_image = rootDir + "/pdf/reddit.png"
    screens_path = rootDir + "/screenshots"
    im = cv2.imread(reddit_image)
    doc = fitz.open(file_path)
    page = doc.load_page(0)
    tp = page.get_textpage()
    blocks = tp.extractBLOCKS()
    divide = "Share\nReport"
    regex_user= r'· \d{1,3} (days|mo.|yr.) ago(.*)$'
    regex_  = r'\d+\n'
    prev_y = 0
    start_margin_x = 6
    constant_x_end = 878
    idx = 0
    prev_block_id = 0
    final = []
    with open("./test.txt", "w") as f:
        json.dump(blocks, f)
    for block_idx, block in enumerate(blocks):
        if re.search(regex_user, block[4]):
            if idx == 0:
                top_cutoff = prev_y * scale  + 20
                bottom_cuttof = int(block[1])* scale
                start_x =int(blocks[prev_block_id][0])* scale - start_margin_x - 20
            else:
                top_cutoff = prev_y * scale
                bottom_cuttof = int(blocks[block_idx - 1][3])* scale
                start_x =int(blocks[prev_block_id][0])* scale - start_margin_x - 5
            curr_y = int(block[1])
            stop_x =constant_x_end * scale
            roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
            prev_y = curr_y
            roi_height =  bottom_cuttof - top_cutoff
            if roi_height > H:
                title_long = []
                if idx == 0:
                    for screen_name_idx, ids in enumerate(range(prev_block_id,block_idx)):
                        top_cutoff = int(blocks[ids][1])* scale
                        bottom_cuttof = int(blocks[ids][3])* scale
                        roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
                        if ids == block_idx - 1:
                            cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" +  str(0) + ".jpg", roi)
                        else:
                            cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" + str(screen_name_idx + 1) + ".jpg", roi)
                        # title_long.append((blocks[ids][0], "LONG COMMENT\n"))
                        title_long.append((blocks[ids][0], blocks[ids][4]))
                    final.append(title_long)
                else:
                    comment_long = []
                    comment_long.append((block[0], block[4]))
                    track_idx = 0
                    for screen_name_idx, ids in enumerate(range(prev_block_id + 1,block_idx - 1)):
                        if screen_name_idx == 0:
                            top_cutoff = int(blocks[ids - 1][1])* scale
                            b = (blocks[ids - 1][0], blocks[ids][4])
                        else:

                            top_cutoff = int(blocks[ids][1])* scale
                            b = (blocks[ids][0], blocks[ids][4])
                        if not re.search(regex_, b[1]):
                            comment_long.append(b)
                            bottom_cuttof = int(blocks[ids][3])* scale
                            roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
                            cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" + str(track_idx) + ".jpg", roi)
                            track_idx += 1
                    final.append(comment_long)
            else:
                cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                for sentence_id in range(prev_block_id, block_idx):
                    if (divide not in blocks[sentence_id][4]):
                        final.append((blocks[sentence_id][0], blocks[sentence_id][4]))
            prev_block_id = block_idx
            idx += 1
    columns = set()
    columns = set([int(x[0]) for x in final if not isinstance(x, list) and re.search(regex_user, x[1])])
    columns = sorted(columns)
    with open(rootDir + "/ssml/edited/ssml_processed.xml", "w") as f:
        f.write("<speak>")
        f.write("<break time=\"1s\"/>\n")
        story_idx = 0
        for line in final:
            if not isinstance(line, list) and re.search(regex_user, line[1]):
                if line[0] == columns[0]:
                    f.write("<break time=\"0.3s\"/>\n")
                    f.write("<mark name=\"STORY" + str(story_idx) + "\"/>\n")
                    f.write("<break time=\"0.3s\"/>\n")
                    story_idx += 1
                f.write("\n")
                f.write("<break time=\"0.1s\"/>\n")
                f.write("<mark name=\"COMMENT\"/>\n")
                f.write("<break time=\"0.1s\"/>\n")
                f.write("\n")
            else:
                if isinstance(line, list):
                    paras = len(line)
                    new_paras = []
                    for para in line:
                        text = cleanTTS(para[1])
                        text = redditAcronyms(text)
                        text = cleanAbreviations(text)
                        if text != "":
                            new_paras.append(text)
                    f.write("<mark name=\"LONG COMMENT\" value=" + "\"" + str(len(new_paras)) + "\"" + "/>\n")
                    for new_text in new_paras:
                        f.write("<mark name=\"PARA\"/>\n")
                        f.write(new_text)
                else:
                    text = cleanTTS(line[1])
                    text = redditAcronyms(text)
                    text = cleanAbreviations(text)
                    f.write(text)
        f.write("</speak>")
    f.close()

