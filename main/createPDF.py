import sys
from utils.pdfSplit import generateScreensSSML
from utils.singlePAge import pdfMergeSInglePage

if __name__ == "__main__":
    rootdir = sys.argv[1]
    print("merge pdf ..")
    pdfMergeSInglePage(rootdir)





