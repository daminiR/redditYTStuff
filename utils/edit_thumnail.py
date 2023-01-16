import sys
#TODO: clculate and add total coments in metadat
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rembg import remove
import random
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

def border (im):
    borderSize = 25
    color = (255, 255, 255)
    alpha = im.getchannel('A')
    # Create red image the same size and copy alpha channel across
    background = Image.new('RGBA', im.size, color=color)
    background.putalpha(alpha)
    # Make the background bigger
    background=background.resize((background.size[0]+borderSize, background.size[1]+borderSize))
    # Merge the targeted image (foreground) with the background
    foreground = im
    background.paste(foreground, (int(borderSize/2), int(borderSize/2)), foreground.convert("RGBA"))
    imageWithBorder = background
    # imageWithBorder.show()
    return imageWithBorder

def createThumbnail(rootDir, text_width, x_offset):
    background = Image.open("./assets/thumbnail/saveBackground.jpg").resize((1280, 720))
    redditIcon = Image.open("./assets/thumbnail/thumbnail_background.png")
    bw, bh = background.size
    input_path = rootDir + "/assets/thumbnail_input_image/image.jpg"
    input = cv2.imread(input_path)
    img = remove(input)
    output_img = Image.fromarray(img)
    # output_img = border(output_img)
    output_img.getbbox()  # (64, 89, 278, 267)
    cropped_pil_img = output_img.crop(output_img.getbbox())
    img_modified = np.asarray(cropped_pil_img)
    final = image_resize(img_modified, height=bh)
    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(final)
    # add border?
    cx = int(bw * 3 / 4)
    pos_x = cx - im_pil.size[0] / 2
    background.paste(im_pil, (int(pos_x), 0))
    background.paste(redditIcon, (10, 10))
    draw = ImageDraw.Draw(background)
    FOREGROUND = (255, 191, 0)
    with open(rootDir +  "/metadata.json" , "rb") as handle:
        data = json.load(handle)
        title_text = data["RedditThumbnailTitle"]
        word_highlights = data["highlights"]
    # more than 18
    words = title_text.split(" ")
    width_text = text_width
    lines = textwrap.wrap(title_text, width=width_text)
    fontSize =  int((bh / (len(lines) + 2) ))
    w, h = background.size
    w = w / 2 + 20
    y_text = 80
    font_path = '/System/Library/Fonts/Supplemental/Impact.ttf'
    font = ImageFont.truetype(font_path, fontSize, encoding='unic')
    red  = (249,97,103)
    green = (76, 187, 23)
    blue =  (25,181,254)
    yellow = (247,202,24)
    highlight_list = [red, green, blue, yellow]
    highlight_fill  = random.choice(highlight_list)
    normal_fill = (242, 243, 245)
    stroke_fill = (0, 0, 0)
    for line in lines:
        width, height = font.getsize(line)
        words = line.split(" ")
        coord_width = 30
        for word in words:
            print(word)
            capital_word = word.upper()
            width_word, _ = font.getsize(capital_word)
            if word in word_highlights:
                draw.text((coord_width , y_text),capital_word,  font=font, fill=highlight_fill, stroke_fill=stroke_fill, stroke_width=9)
            else:
                draw.text((coord_width , y_text),capital_word,  font=font, fill=normal_fill, stroke_fill=stroke_fill, stroke_width=9)
            coord_width = coord_width + width_word + x_offset
        y_text += height + 10
    background.save(rootDir + "/youtubeVideo/thumbnail_v2.jpg")

