import json
import re
import os

def converToJSON(redditFolder):
    outFile = 'marks_processed.json'
    inputFile = os.path.join(redditFolder, '/marks/original/marks.json')
    with open(os.path.join(redditFolder, '/marks/original/marks.json'), 'r') as input, open(redditFolder + '/marks/edited/' + outFile, 'w+') as output:
        output.write("[\n")
        for line in input:
            line = re.sub('}\n', '},\n', line)
            output.write('    '+line)
        output.write("]\n")

