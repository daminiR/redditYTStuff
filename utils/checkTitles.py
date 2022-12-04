import os, sys
import json
rootFOlder = "/Users/daminirijhwani/redditYTStuff/TTSData/ytData"
from difflib import SequenceMatcher

def checkTitle(testTitle):
    for (dirpath, dirnames, filenames) in os.walk(rootFOlder):
        for filename in filenames:
            if filename == "metadata.json":
                with open(os.path.join(dirpath, filename), 'r') as metaData:
                    title = json.load(metaData)["RedditTitle"]
                    sequenceRatio = SequenceMatcher(None, testTitle, title).ratio()
                    if sequenceRatio > 0.8:
                        print(sequenceRatio)
                        print(dirpath)
                        return  True



if __name__ == "__main__":
    testTitle = sys.argv[1]
    checkTitle(testTitle)
