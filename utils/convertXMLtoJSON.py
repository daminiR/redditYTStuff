import json
import re
import os

def converToJSON(redditFolder):
    outFile = 'marks_processed.json'
    inputFile = redditFolder + "/marks/original/marks.json"
    with open(inputFile, 'r') as input, open(redditFolder + '/marks/edited/' + outFile, 'w+') as output:
        output.write("[\n")
        lines = input.readlines()
        last = lines[-1]
        for line in lines:
            if line is last:
                line = re.sub('}\n', '}\n', line)
                output.write('    '+line)
            else:
                line = re.sub('}\n', '},\n', line)
                output.write('    '+line)
        output.write("]\n")

