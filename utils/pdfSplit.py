import os
import fitz
import cv2
import json
import re

def convertToBox(x1, y1, x2, y2):
    return [int((x2 + x1)/2 ), int((y2 + y1)/2), int(x2 - x1), int(y2 - y1)]

def cleanTTS(line):
    if "Comment deleted" in line:
        print("Remove these")
        print(line)
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
    # if re.search(regex_numbers,new):
        # new = re.sub(regex_user,  "", new)
        # new = ""
    return new


def generateScreensSSML(rootDir):
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
    # divide_deleted_user = "Share\nReport\nSave"
    title_divide = "Comments\n� Award\n� Share\n"
    title_start = "Posted by u/"
    regex_user= r'· \d{1,3} (days|mo.|yr.) ago(.*)$'
    regex_replies = r'^\d{0,10} more reply|replies$'
    prev_y = 0
    start_margin_x = 5
    constant_x_end = 825
    top_margin = 11
    idx = 1
    prev_block_id = 0
    final = []
    with open("./test.txt", "w") as f:
        json.dump(blocks, f)
    for block_idx, block in enumerate(blocks):
        if (divide not in block[4]) and not re.search(regex_replies, block[4]):
            final.append([block[0], block[4]])
        if divide in block[4]:
            last_reply_block = None
            for ids in range(prev_block_id, block_idx):
                check = blocks[ids]
                first_comment = re.search(regex_user, check[4])
                if re.search(regex_replies, check[4]):
                    last_reply_block = check
                    track_replies_y = int(block[3])
                if title_divide in check[4] and idx == 1:
                    title_block = check
                    track_clock_y = int(block[3])
                if title_start in check[4] and idx == 1:
                    title_start_block = check
                if first_comment and idx == 1:
                    start_first_comment = check
            if last_reply_block:
                top_cutoff = int(last_reply_block[3])
            else:
                top_cutoff = prev_y + top_margin
            curr_y = int(block[3])
            start_x =int( block[0])
            stop_x =int( block[2])
            roi=im[top_cutoff*scale:curr_y*scale,start_x*scale - start_margin_x*scale: constant_x_end*scale]
            prev_y = curr_y
            prev_block_id = block_idx
            try:
                if idx == 1:
                    cutOff_title = int(title_block[3])
                    start_title_y = int(title_start_block[3])
                    start_comment_y = int(start_first_comment[3])
                    roi1=im[start_title_y*scale:cutOff_title*scale,start_x*scale - start_margin_x*scale: constant_x_end*scale]
                    roi2=im[start_comment_y*scale:curr_y*scale,start_x*scale - start_margin_x*scale: constant_x_end*scale]
                    cv2.imwrite(screens_path + "/screen_" + str(0) + ".jpg", roi1)
                    cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi2)
                else:
                    cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
            except Exception as e:
                    print(e)
                    pass
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
                # clean line before writing
                text = cleanTTS(line[1])
                f.write(text)
        f.write("</speak>")
    f.close()

