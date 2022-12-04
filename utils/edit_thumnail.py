import sys
#TODO: clculate and add total coments in metadat
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rembg import remove
import textwrap
import numpy as np
import cv2
import json

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def createThumbnail(rootDir):
    background = Image.open("./assets/thumbnail/saveBackground.jpg").resize((1280, 720))
    redditIcon = Image.open("./assets/thumbnail/thumbnail_background.png")
    bw, bh = background.size
    input_path = rootDir + "/assets/thumbnail_input_image/image.jpg"
    input = cv2.imread(input_path)
    img = remove(input)
    output_img = Image.fromarray(img)
    output_img.getbbox()  # (64, 89, 278, 267)
    cropped_pil_img = output_img.crop(output_img.getbbox())
    img_modified = np.asarray(cropped_pil_img)
    final = image_resize(img_modified, height=bh)
    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(final)
    cx = int(bw * 3 / 4)
    pos_x = cx - im_pil.size[0] / 2
    background.paste(im_pil, (int(pos_x), 0))
    background.paste(redditIcon, (10, 10))
    draw = ImageDraw.Draw(background)
    FOREGROUND = (255, 191, 0)
    with open(rootDir +  "/metadata.json" , "rb") as handle:
        data = json.load(handle)
        title_text = data["RedditTitle"]
        word_highlights = data["highlights"]

    # more than 18
    words = title_text.split(" ")
    if len(words) < 25:
        width_text = 15
    elif len(words) >= 25 and len(words) < 30:
        width_text = 21
    elif len(words) >= 30 and len(words) < 50:
        width_text = 28
    else:
        width_text = 30

    lines = textwrap.wrap(title_text, width=width_text)
    fontSize =  int(bh / (len(lines) + 4))
    w, h = background.size
    w = w / 2 + 20
    y_text = 90
    font_path = '/Users/daminirijhwani/Library/Fonts/C1C06396-FFAC-4A4F-B2ED-4ECD3798A4E6.localized/Cabin-Bold.otf'
    font = ImageFont.truetype(font_path, fontSize, encoding='unic')
    highlight_fill  = (249,97,103)
    highlight_stroke = (104,55,57)
    normal_fill = FOREGROUND
    normal_stroke  = (168, 127, 3)

    for line in lines:
        width, height = font.getsize(line)
        coord_width = 30
        for word in line.split(" "):
            width_word, _ = font.getsize(word)
            if word in word_highlights:
                draw.text((coord_width , y_text),word,  font=font, fill=highlight_fill, stroke_width=4, stroke_fill=highlight_stroke)
            else:
                draw.text((coord_width , y_text),word,  font=font, fill=normal_fill, stroke_width=3, stroke_fill=normal_stroke)
            coord_width = coord_width + width_word + 30
        y_text += height
    background.save(rootDir + "/youtubeVideo/thumbnail.jpg")

