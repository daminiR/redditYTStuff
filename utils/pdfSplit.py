import os
import fitz
import cv2
import json
import re

def convertToBox(x1, y1, x2, y2):
    return [int((x2 + x1)/2 ), int((y2 + y1)/2), int(x2 - x1), int(y2 - y1)]

def generateScreensSSML(rootDir):
    file_path = rootDir + "/pdf/reddit_single_page.pdf"
    reddit_image = rootDir + "/pdf/reddit.png"
    screens_path = rootDir + "/screenshots"
    im = cv2.imread(reddit_image)
    doc = fitz.open(file_path)
    page = doc.load_page(0)
    tp = page.get_textpage()
    blocks = tp.extractBLOCKS()
    divide = "Reply\nGive Award\nShare\nReport\nSave\nFollow"
    more_replies = "more replies"
    prev_y = 0
    start_margin_x = 5
    constant_x_end = 825
    top_margin = 11
    idx = 0
    track_replies_y = 0
    prev_block_id = 0
    regex = r'^([^\s]+ · \d{1,3} ((\bdays\b)|(\bmn.\b)) ago)(.*)$'
    final = []
    with open("./test.txt", "w") as f:
        json.dump(blocks, f)
    for block_idx, block in enumerate(blocks):
        print(block)
        if divide not in block[4] and more_replies not in block[4]:
            final.append([block[0], block[4]])
        if divide in block[4]:
            print(block)
            last_reply_block = None
            for ids in range(prev_block_id, block_idx):
                check = blocks[ids]
                if more_replies in check[4]:
                    last_reply_block = check
                    track_replies_y = int(block[3])
            if last_reply_block:
                top_cutoff = int(last_reply_block[3])
            else:
                top_cutoff = prev_y + top_margin
            curr_y = int(block[3])
            print(curr_y)
            start_x =int( block[0])
            stop_x =int( block[2])
            roi=im[top_cutoff:curr_y,start_x - start_margin_x: constant_x_end]
            prev_y = curr_y
            prev_block_id = block_idx
            try:
                cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                cv2.close()
            except:
                pass
            idx += 1
            break
    columns = set([int(x[0]) for x in final if re.search(regex, x[1])])
    columns = sorted(columns)
    with open(rootDir + "/ssml/ssml_processed.xml", "w") as f:
        f.write("<speak>")
        f.write("<break time=\"0.3s\"/>\n")
        for line in final:
            x = re.search(regex, line[1])
            if x:
                # if line[0] == columns[0]:
                    # print(line)
                f.write("\n")
                f.write("<break time=\"0.3s\"/>\n")
                f.write("<mark name=\"COMMENT\"/>\n")
                f.write("<break time=\"0.3s\"/>\n")
                f.write("\n")
            else:
                f.write(line[1])
        f.write("</speak>")
    f.close()

