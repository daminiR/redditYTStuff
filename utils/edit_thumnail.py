import sys
#TODO: clculate and add total coments in metadat
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rembg import remove
import textwrap

import json
def createThumbnail(rootDir, fontSize):
    background = Image.open("./assets/thumbnail/saveBackground.jpg").resize((1280, 720))
    redditIcon = Image.open("./assets/thumbnail/thumbnail_background.png")
    bw, bh = background.size
    input_path = rootDir + "/assets/thumbnail_input_image/image.jpg"
    input = Image.open(input_path).resize((int(bw * 2 / 3), bh))
    img = remove(input)
    background.paste(img, (int(bw / 3), 0))
    background.paste(redditIcon, (10, 10))
    draw = ImageDraw.Draw(background)
    FOREGROUND = (255, 191, 0)
    with open(rootDir +  "/metadata.json" , "rb") as handle:
        data = json.load(handle)
        print(data)
        title_text = data["RedditTitle"]
        word_highlights = data["highlights"]
    lines = textwrap.wrap(title_text, width=15)
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
        coord_width =30
        for word in line.split(" "):
            width_word, _ = font.getsize(word)
            if word in word_highlights:
                draw.text((coord_width , y_text),word,  font=font, fill=highlight_fill, stroke_width=4, stroke_fill=highlight_stroke)
            else:
                draw.text((coord_width , y_text),word,  font=font, fill=normal_fill, stroke_width=3, stroke_fill=normal_stroke)
            coord_width = coord_width + width_word + 30
        y_text += height
    background.save(rootDir + "/youtubeVideo/thumbnail.jpg")

