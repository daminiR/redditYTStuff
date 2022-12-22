import sys
#TODO: clculate and add total coments in metadat
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rembg import remove
import textwrap
from utils.edit_thumnail import createThumbnail

import json
if __name__ == "__main__":
    rootDir = sys.argv[1]
    text_width = 17
    x_offset = 64
    if len(sys.argv) == 3:
        text_width = int(sys.argv[2])
    if len(sys.argv) == 4:
        text_width = int(sys.argv[2])
        x_offset = int(sys.argv[3])
    createThumbnail(rootDir, text_width, x_offset)


