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
    fontSize = sys.argv[2]
    createThumbnail(rootDir, int(fontSize))


