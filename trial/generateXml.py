import os
import fitz
import cv2
import json

def convertToBox(x1, y1, x2, y2):
    return [int((x2 + x1)/2 ), int((y2 + y1)/2), int(x2 - x1), int(y2 - y1)]


file_path = "./out.pdf"
im = cv2.imread('out.png')
doc = fitz.open(file_path)
page = doc.load_page(0)
tp = page.get_textpage()
blocks = tp.extractXHTML()()
divide = "Reply\nGive Award\nShare\nReport\nSave\nFollow"
more_replies = "more replies"
prev_y = 0
start_margin_x = 5
constant_x_end = 825
top_margin = 11
idx = 0
track_replies_y = 0
prev_block_id = 0
for block_idx, block in enumerate(blocks):
    if divide in block[4]:
        # if idx == 12:
            # break
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
        start_x =int( block[0])
        stop_x =int( block[2])
        roi=im[top_cutoff:curr_y,start_x - start_margin_x: constant_x_end]
        prev_y = curr_y
        prev_block_id = block_idx
        try:
            cv2.imwrite("./screeshots/screen_" + str(idx) + ".jpg", roi)
        except:
            pass
        idx += 1
        # break


