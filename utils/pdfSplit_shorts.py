import os
import fitz
import cv2
import json
import re
from moviepy.editor import VideoFileClip
from utils.checkTitles import checkTitle
from utils.textCleanup import *
longTitles = ["AITA", "TwoSentenceHorror", "TIFU", "relationship_advice"]
shortTitles = ["AskReddit"]

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
    regex_  = r'\d+\n'
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
            if roi_height > H:
                if any(ext in rootDir for ext in longTitles):
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
                    pass
            else:
                try:
                    cv2.imwrite(screens_path + "/screen_" + str(idx) + ".jpg", roi)
                except:
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
                f.write("<break time=\"0.05s\"/>\n")
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
                    try:
                        f.write(text)
                    except:
                        pass
        f.write("</speak>")

