import sys
from utils.pdfSplit import generateScreensSSML

if __name__ == "__main__":
    rootdir = sys.argv[1]
    print("geenrate ssml and screenshots ...")
    generateScreensSSML(rootdir)
