import os
import fitz
import cv2
import json
import re
from moviepy.editor import VideoFileClip
from utils.checkTitles import checkTitle
longTitles = ["AITA", "TwoSentenceHorror", "TIFU"]
shortTitles = ["AskReddit"]

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
    new = new.replace("AMA", "Ask Me Anything")
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
    # bad words
    new = new.replace("Fuck", "f-")
    new = new.replace("fuck", "f-")
    new = new.replace("asshole", "ahole")
    new = new.replace("asshole", "ahole")
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
    regex_user= r'Comment deleted by user · \d{1,3} (min.|day|days|mo.|yr.|hr.) ago(.*)'
    regex_hidden_user = r'· \d{1,3} (min.|day|days|mo.|yr.|hr.) ago(.*)$'
    regex_comments=r'^\d{1,5}.\dk$'
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
        print(new)
        new = ""
    if re.search(regex_more,new):
        print(new)
        new = ""
    if re.search(regex_hidden_user,new):
        print(new)
        new = ""
    return new

def clean(blocks):
    regex_  = r'^\d+\n$'
    regex_2  = r'^\d+ & \d+ More\n$'
    new_blocks = []
    for block in blocks:
        if not re.search(regex_, block[4]) and not re.search(regex_2, block[4]):
            new_blocks.append(block)
    return new_blocks

def generateScreensShorts(rootDir,filename_pdf):
    metaDataDict = json.load(open(os.path.join(rootDir, 'metadata.json'), "r"))
    filename = metaDataDict['videoFileUsed']
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollection/"
    videoPath=os.path.join(videoCollection, filename)
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    H = backgroundVideoSize[1]
    scale = 2
    file_path = rootDir + "/pdf/" + filename_pdf
    reddit_image = rootDir + "/pdf/reddit_shorts.png"
    screens_path = rootDir + "/screenshots_shorts"
    im = cv2.imread(reddit_image)
    doc = fitz.open(file_path)
    page = doc.load_page(0)
    tp = page.get_textpage()
    blocks = tp.extractBLOCKS()
    divide = "Share"
    regex_user= r'\d{1,3} (min.|day|days|mo.|yr.|hr.) ago(.*)$'
    prev_y = 0
    start_margin_x = 6
    constant_x_end = 878
    idx = 0
    prev_block_id = 0
    final = []
    blocks = clean(blocks)
    metadataFile = rootDir + "/metadata.json"
    MAX_LENGTH = 50
    for block_idx, block in enumerate(blocks):
        if re.search(regex_user, block[4]):
            if idx == MAX_LENGTH:
                break
            if idx == 0:
                    top_cutoff = int(blocks[prev_block_id][1]) * scale
                    bottom_cuttof = int(blocks[prev_block_id][3]) * scale
                    start_x = int(blocks[prev_block_id][0]) * scale
            else:
                top_cutoff = prev_y * scale
                bottom_cuttof = int(blocks[block_idx - 1][3])* scale
                start_x =int(blocks[prev_block_id][0])* scale - start_margin_x - 5
            curr_y = int(block[1])
            stop_x =constant_x_end * scale
            roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
            prev_y = curr_y
            roi_height =  bottom_cuttof - top_cutoff
            if roi_height > int(H / 2):
                pass
            else:
                try:
                    cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                except:
                    print("didn't work?")
                    print(block)
                    continue
                full_text = []
                for sentence_id in range(prev_block_id, block_idx):
                    if (divide not in blocks[sentence_id][4]):
                        full_text.append((blocks[sentence_id][0], blocks[sentence_id][4]))
                if prev_block_id == 0:
                    title = [full_text[-1]]
                    title.extend(full_text[:-1])
                    full_text = title
                final.extend(full_text)
                idx += 1
            prev_block_id = block_idx
    columns = set()
    columns = set([int(x[0]) for x in final if not isinstance(x, list) and re.search(regex_user, x[1])])
    columns = sorted(columns)
    with open(rootDir + "/ssml/edited/ssml_processed_shorts.xml", "w") as f:
        f.write("<speak>")
        f.write("<break time=\"1s\"/>\n")
        f.write("<mark name=\"TITLE\"/>\n")
        story_idx = 0
        for line_idx, line in enumerate(final):
            if not isinstance(line, list) and re.search(regex_user, line[1]):
                f.write("\n")
                f.write("<break time=\"0.1s\"/>\n")
                f.write("<mark name=\"COMMENT\"/>\n")
                f.write("\n")
            else:
                if isinstance(line, list):
                    paras = len(line)
                    new_paras = []
                    for title_ids, para in enumerate(line):
                        if title_ids == len(line) - 1 and line_idx == 0:
                            metaDataTitle = para[1]
                            handle = open(metadataFile, 'r')
                            oldMetaData = json.load(handle)
                            y = {'RedditTitle' : metaDataTitle}
                            oldMetaData.update(y)
                            add = open(metadataFile, 'w')
                            json.dump(oldMetaData, add, indent=4)
                            handle.close()
                        # text = cleanEmoji(para[1], no_emoji=True)
                        text = cleanTTS(para[1])
                        text = redditAcronyms(text)
                        text = cleanAbreviations(text)
                        if text != "":
                            new_paras.append(text)
                    if line_idx == 0:
                        title = [new_paras[-1]]
                        # check if title is not done previosuly
                        # isInReddit = checkTitle(title)
                        # assert (isInReddit == False),"the title is already made into youtube video or check folder to be sure"
                        title.extend(new_paras[:-1])
                        new_paras = title
                    f.write("<mark name=\"LONG COMMENT START" + str(len(new_paras)) + "\"" + "/>\n")
                    for new_text_idx, new_text in enumerate(new_paras):
                        f.write("\n<mark name=\"PARA\"/>\n")
                        f.write(new_text)
                        if line_idx == 0 and new_text_idx == 0:
                            f.write("\n<break time=\"0.5s\"/>\n")
                        else:
                            f.write("\n<break time=\"0.2s\"/>\n")
                    f.write("\n<mark name=\"LONG COMMENT END" + str(len(new_paras)) + "\"" + "/>\n")
                else:
                    text = cleanTTS(line[1])
                    text = redditAcronyms(text)
                    text = cleanAbreviations(text)
                    f.write(text)
        f.write("</speak>")

def generateScreensSSML(rootDir,filename_type):
    metaDataDict = json.load(open(os.path.join(rootDir, 'metadata.json'), "r"))
    filename = metaDataDict['videoFileUsed']
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollection/"
    videoPath=os.path.join(videoCollection, filename)
    backgroundVideo = VideoFileClip(videoPath)
    backgroundVideoSize = backgroundVideo.size
    H = backgroundVideoSize[1]
    scale = 2
    file_path = rootDir + "/pdf/" + filename_type
    reddit_image = rootDir + "/pdf/reddit.png"
    screens_path = rootDir + "/screenshots"
    im = cv2.imread(reddit_image)
    doc = fitz.open(file_path)
    page = doc.load_page(0)
    tp = page.get_textpage()
    blocks = tp.extractBLOCKS()
    divide = "Share\nReport"
    regex_user= r'\d{1,3} (min.|day|days|mo.|yr.|hr.) ago(.*)$'
    regex_  = r'\d+\n'
    prev_y = 0
    start_margin_x = 6
    constant_x_end = 878
    idx = 0
    prev_block_id = 0
    final = []
    blocks = clean(blocks)
    metadataFile = rootDir + "/metadata.json"
    for block_idx, block in enumerate(blocks):
        if re.search(regex_user, block[4]):
            if idx == 0:
                if any(ext in rootDir for ext in shortTitles):
                    top_cutoff = int(blocks[prev_block_id][1]) * scale
                    bottom_cuttof = int(blocks[prev_block_id][3]) * scale
                    start_x = int(blocks[prev_block_id][0]) * scale
                if any(ext in rootDir for ext in longTitles):
                # old code that probabaly works with list long para
                    top_cutoff = prev_y * scale + 120
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
            if roi_height > H -100:
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
                            try:
                                comment_long.append(b)
                                bottom_cuttof = int(blocks[ids][3])* scale
                                roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
                                cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" + str(track_idx) + ".jpg", roi)
                                track_idx += 1
                            except:
                                pass
                    final.append(comment_long)
                prev_block_id = block_idx
                idx += 1
            else:
                try:
                    cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                    full_text = []
                    for sentence_id in range(prev_block_id, block_idx):
                        if (divide not in blocks[sentence_id][4]):
                            full_text.append((blocks[sentence_id][0], blocks[sentence_id][4]))
                    if prev_block_id == 0:
                        title = [full_text[-1]]
                        title.extend(full_text[:-1])
                        full_text = title
                    final.extend(full_text)
                    prev_block_id = block_idx
                    idx += 1
                except:
                    pass
    columns = set()
    columns = set([int(x[0]) for x in final if not isinstance(x, list) and re.search(regex_user, x[1])])
    columns = sorted(columns)
    with open(rootDir + "/ssml/edited/ssml_processed.xml", "w") as f:
        f.write("<speak>")
        f.write("<break time=\"1s\"/>\n")
        f.write("<mark name=\"TITLE\"/>\n")
        story_idx = 0
        for line_idx, line in enumerate(final):
            if not isinstance(line, list) and re.search(regex_user, line[1]):
                if line[0] == columns[0]:
                    f.write("<break time=\"0.2s\"/>\n")
                    f.write("<mark name=\"STORY" + str(story_idx) + "\"/>\n")
                    f.write("<break time=\"0.2s\"/>\n")
                    story_idx += 1
                f.write("\n")
                f.write("<break time=\"0.05s\"/>\n")
                f.write("<mark name=\"COMMENT\"/>\n")
                f.write("<break time=\"0.05s\"/>\n")
                f.write("\n")
            else:
                if isinstance(line, list):
                    paras = len(line)
                    new_paras = []
                    for title_ids, para in enumerate(line):
                        if title_ids == len(line) - 1 and line_idx == 0:
                            metaDataTitle = para[1]
                            handle = open(metadataFile, 'r')
                            oldMetaData = json.load(handle)
                            y = {'RedditTitle' : metaDataTitle}
                            oldMetaData.update(y)
                            add = open(metadataFile, 'w')
                            json.dump(oldMetaData, add, indent=4)
                            handle.close()
                        # text = cleanEmoji(para[1], no_emoji=True)
                        text = cleanTTS(para[1])
                        text = redditAcronyms(text)
                        text = cleanAbreviations(text)
                        if text != "":
                            new_paras.append(text)
                    if line_idx == 0:
                        title = [new_paras[-1]]
                        # check if title is not done previosuly
                        # isInReddit = checkTitle(title)
                        # assert (isInReddit == False),"the title is already made into youtube video or check folder to be sure"
                        title.extend(new_paras[:-1])
                        new_paras = title
                    f.write("<mark name=\"LONG COMMENT START" + str(len(new_paras)) + "\"" + "/>\n")
                    for new_text_idx, new_text in enumerate(new_paras):
                        f.write("\n<mark name=\"PARA\"/>\n")
                        f.write(new_text)
                        if line_idx == 0 and new_text_idx == 0:
                            f.write("\n<break time=\"0.5s\"/>\n")
                        # else:
                            # f.write("\n<break time=\"0.2s\"/>\n")
                    f.write("\n<mark name=\"LONG COMMENT END" + str(len(new_paras)) + "\"" + "/>\n")
                else:
                    if line_idx == 0:
                        # check if title is not done previosuly
                        metaDataTitle = line[1]
                        # isInReddit = checkTitle(metaDataTitle)
                        # assert (isInReddit == False),"the title is already made into youtube video or check folder to be sure"
                        handle = open(metadataFile, 'r')
                        oldMetaData = json.load(handle)
                        y = {'RedditTitle' : metaDataTitle}
                        oldMetaData.update(y)
                        add = open(metadataFile, 'w')
                        json.dump(oldMetaData, add, indent=4)
                        handle.close()
                    # text = cleanEmoji(line[1], no_emoji=True)
                    text = cleanTTS(line[1])
                    text = redditAcronyms(text)
                    text = cleanAbreviations(text)
                    try:
                        f.write(text)
                    except:
                        pass
        f.write("</speak>")
    f.close()

