import sys
from utils.pdfSplit import generateScreensSSML, generateScreensShorts

if __name__ == "__main__":
    rootdir = sys.argv[1]
    videoType = sys.argv[2]
    if videoType == 'short':
        print("geenrate ssml and screenshots for shorts ...")
        generateScreensShorts(rootdir, "reddit_shorts_single_page.pdf")
    elif videoType == 'long':
        print("geenrate ssml and screenshots for long ...")
        generateScreensSSML(rootdir, "reddit_single_page.pdf")
