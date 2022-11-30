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
    title_divide = "Comments\n� Award\n� Share\n"
    title_start = "Posted by u/"
    regex_user= r'· \d{1,3} (days|mo.|yr.) ago(.*)$'
    regex_replies = r'^\d{0,10} more reply|replies$'
    prev_y = 0
    start_margin_x = 6
    constant_x_end = 878
    top_margin = 11
    idx = 1
    prev_block_id = 0
    final = []
    with open("./test.txt", "w") as f:
        json.dump(blocks, f)
    for block_idx, block in enumerate(blocks):
        if (divide not in block[4]) and not re.search(regex_replies, block[4]):
            final.append([block[0], block[4]])
        if re.search(regex_user, block[4]) or divide in block[4]:
            if re.search(regex_user, block[4]):
                last_reply_block = None
                if idx == 1:
                    top_cutoff = prev_y * scale  + 20
                else:
                    top_cutoff = prev_y * scale
                curr_y = int(block[1])
                start_x =int(blocks[prev_block_id][0])* scale - start_margin_x
                stop_x =constant_x_end * scale
                print(blocks[block_idx - 1])
                roi=im[top_cutoff:curr_y*scale,start_x: stop_x]
                prev_y = curr_y
                print(block)
                # if idx == 1:
                    # cutOff_title = int(title_block[3])
                    # start_title_y = int(title_start_block[3])
                    # start_comment_y = int(start_first_comment[3])
                    # roi1=im[start_title_y*scale:cutOff_title*scale,        start_x*scale - start_margin_x*scale: constant_x_end*scale]
                    # roi2=im[start_comment_y*scale:curr_y*scale,            start_x*scale - start_margin_x*scale: constant_x_end*scale]
                    # roi1_height =  ( cutOff_title - start_title_y )*scale
                    # roi2_height =  (start_comment_y - curr_y )*scale
                    # if roi1_height > H:
                        # prev_para_y = start_title_y
                        # print(title_start_id, title_block_id)
                        # for ids in range(title_start_id, title_block_id):
                            # print(ids)
                            # para = blocks[ids]
                            # print(para)
                            # end_para = int(para[3])
                            # roi=im[prev_para_y*scale:end_para*scale,        start_x*scale - start_margin_x*scale: constant_x_end*scale]
                            # cv2.imshow('image',roi)
                            # cv2.waitKey(0)
                            # prev_para_y = end_para
                    # else:
                        # cv2.imwrite(screens_path + "/screen_" + str(0) + ".jpg", roi1)
                    # if roi2_height > H:
                        # print("do we eneter here")
                        # prev_para_y = start_comment_y
                        # for ids in range(prev_block_id, block_idx):
                                # para = blocks[ids]
                                # end_para = int(para[3])
                                # roi=im[prev_para_y*scale:end_para*scale,        start_x*scale - start_margin_x*scale: constant_x_end*scale]
                                # cv2.imshow('image',roi)
                                # cv2.waitKey(0)
                                # prev_para_y = end_para
                    # else:
                        # cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi2)
                # else:
                roi_height =  (curr_y - top_cutoff )*scale
                # if roi_height > H:
                    # prev_para_y = top_cutoff
                    # for ids in range(prev_block_id + 2, block_idx):
                            # para = blocks[ids]
                            # end_para = int(para[3])
                            # roi_para=im[prev_para_y*scale:end_para*scale,start_x*scale - start_margin_x*scale: constant_x_end*scale]
                            # cv2.imshow('image',roi_para)
                            # cv2.waitKey(0)
                            # prev_para_y = end_para
                # else:
                    # cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                cv2.imshow('image',roi)
                cv2.waitKey(0)
                # except Exception as e:
                        # print(e)
                        # pass
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
                text = cleanTTS(line[1])
                f.write(text)
        f.write("</speak>")
    f.close()

