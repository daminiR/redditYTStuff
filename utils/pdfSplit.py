import os
import fitz
import cv2
import json
import re
from moviepy.editor import VideoFileClip

def convertToBox(x1, y1, x2, y2):
    return [int((x2 + x1)/2 ), int((y2 + y1)/2), int(x2 - x1), int(y2 - y1)]

def cleanTTS(line):
    # if "Comment deleted" in line:
        # print("Remove these")
        # print(line)
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
    # regex_numbers=r'^&amp; \d{1,3} More$'
    # regex_numbers=r'^(\d{0,3}((&amp;| &amp;) \d{1,3} More)*)$'
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
    regex_replies = r'^\d{0,10} more reply|replies$'
    prev_y = 0
    start_margin_x = 6
    constant_x_end = 878
    idx = 1
    prev_block_id = 0
    final = []
    longComments = []
    with open("./test.txt", "w") as f:
        json.dump(blocks, f)
    for block_idx, block in enumerate(blocks):
        if re.search(regex_user, block[4]):
            if idx == 1:
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
                final.append([block[0], block[4]])
                final.append([block[0], "LONG COMMENT\n"])
                if idx == 1:
                    for screen_name_idx, ids in enumerate(range(prev_block_id,block_idx)):
                        top_cutoff = int(blocks[ids][1])* scale
                        bottom_cuttof = int(blocks[ids][3])* scale
                        final.append([blocks[ids][0], blocks[ids][4]])
                        final.append([blocks[ids][0], "LONG COMMENT\n"])
                        roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
                        if ids == block_idx - 1:
                            cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" +  str(0) + ".jpg", roi)
                        else:
                            cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" + str(screen_name_idx + 1) + ".jpg", roi)
                else:
                    for screen_name_idx, ids in enumerate(range(prev_block_id + 1,block_idx - 1)):
                        if screen_name_idx == 0:
                            top_cutoff = int(blocks[ids - 1][1])* scale
                            final.append([blocks[ids - 1][0], blocks[ids][4]])
                            final.append([blocks[ids - 1][0], "LONG COMMENT\n"])
                        else:
                            top_cutoff = int(blocks[ids][1])* scale
                            final.append([blocks[ids][0], blocks[ids][4]])
                            final.append([blocks[ids][0], "LONG COMMENT\n"])
                        bottom_cuttof = int(blocks[ids][3])* scale
                        roi=im[top_cutoff:bottom_cuttof,start_x: stop_x]
                        cv2.imwrite(screens_path + "/screen_" + str(idx) + "_" + str(screen_name_idx) + ".jpg", roi)
            else:
                cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                for sentence_id in range(prev_block_id, block_idx):
                    if (divide not in blocks[sentence_id][4]):
                        final.append([blocks[sentence_id][0], blocks[sentence_id][4]])
            prev_block_id = block_idx
            idx += 1
    columns = set([int(x[0]) for x in final if re.search(regex_user, x[1])])
    columns = sorted(columns)
    with open(rootDir + "/ssml/edited/ssml_processed.xml", "w") as f:
        f.write("<speak>")
        f.write("<break time=\"1s\"/>\n")
        story_idx = 1
        for line in final:
            x = re.search(regex_user, line[1])
            if x:
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
                if "LONG COMMENT" in line[1]:
                    f.write("<mark name=\"LONG COMMENT\"/>\n")
                else:
                    text = cleanTTS(line[1])
                    f.write(text)
        f.write("</speak>")
    f.close()

