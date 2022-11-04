import sys
from amazonTextract.exract import extractTextIds
if __name__ == "__main__":
    rootDir = sys.argv[1]
    print("getting img task Ids")
    extractTextIds(rootDir)


