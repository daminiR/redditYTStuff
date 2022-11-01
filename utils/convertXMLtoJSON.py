import json
import re
dirRedditXML= '../OCt_30_2022/reddit_yt_2'
outFile = 'reddit_marks_process.json'
with open('../OCt_30_2022/reddit_yt_2/marks/reddit_mask.json', 'r') as input, open(dirRedditXML + '/' + outFile, 'w') as output:
    output.write("[\n")
    for line in input:
        line = re.sub('}\n', '},\n', line)
        output.write('    '+line)
    output.write("]\n")

