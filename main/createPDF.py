import sys
from utils.singlePAge import pdfMergeSInglePage

if __name__ == "__main__":
    rootdir = sys.argv[1]
    videoType = sys.argv[2]
    print("merge pdf ..")
    if videoType == 'short':
        pdfMergeSInglePage(rootdir, "reddit_shorts.pdf")
    elif videoType == 'long':
        pdfMergeSInglePage(rootdir, "reddit.pdf")
    elif videoType == 'tiktok':
        pdfMergeSInglePage(rootdir, "reddit_tiktok.pdf")





