import os
from xml.dom import minidom
import sys
import os, random
import json

if __name__ == "__main__":
    rootDir = sys.argv[1]
    videoCollection = "/Users/daminirijhwani/redditYTStuff/assets/backgroundVideosCollection/"
    filename = random.choice([f for f in os.listdir(videoCollection) if not f.startswith('.') and f.endswith('.mp4')])
    y = {'videoFileUsed': filename}
    with open(os.path.join(rootDir, 'metadata.json'), "w") as f:
        json.dump(y, f)
    f.close()

