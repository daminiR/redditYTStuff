import sys
from editing.xmlPreprocessing import xmlTreeModifier
if __name__ == "__main__":
    rootDir = sys.argv[1]
    xmlTreeModifier(rootDir)


