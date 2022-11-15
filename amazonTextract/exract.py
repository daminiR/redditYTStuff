from amazonTextract.TextractWrapper import TextractWrapper
from boto3 import Session
import json
import os

# get an approriate etxtID that can be referenced in marks xml
def extractTextId(redditFolder, filename):
    session = Session(profile_name="default")
    textract = session.client("textract")
    s3 = session.client("s3")
    sqs = session.client("sqs")
    textIns = TextractWrapper(textract, s3, sqs)
    response = textIns.detect_file_text(document_file_name=redditFolder + "/screenshots/" + filename)
    blocks = response["Blocks"]
    textIdList = ""
    line_idx = 0
    for idx, block in enumerate(blocks):
        if block["BlockType"] == "LINE":
            text =  block["Text"]
            ### Big Bug Here --- canot use ago  because some
            ##bloacks of senetence contain
            ## ago inseatd use first line since no username is longer than firat lin ein reddit
            if line_idx == 0:
                user = text.split(" ")[0]
                line_idx += 1
            else:
                if not text.isnumeric():
                    textIdList =  textIdList + text
                    if len(textIdList.split(" ")) > 7:
                        break

    text = " ".join(textIdList.split(" ")[:7])
    print("text", text)
    idDict = {"File": filename.split(".")[0],
              "TaskId": text}
    return idDict

def extractTextIds(redditFolder):
    taskIds = []
    for (dirpath, dirnams, filenames) in os.walk(redditFolder + '/screenshots'):
            for filename in filenames:
                    taskIdDict = extractTextId(redditFolder, filename)
                    taskIds.append(taskIdDict)
    IdsDict = {"TaskIds": taskIds}
    f= open(redditFolder + "/screenShotIds/tastIds" +".json", 'w+')
    json.dump(IdsDict, f, indent=4)
    f.close()
    # filename = "Screenshot from 2022-11-07 21-28-07.png"
    # taskIdDict = extractTextId(redditFolder, filename)


