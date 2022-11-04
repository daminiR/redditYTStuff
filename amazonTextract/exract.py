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
    textIdList = []
    for idx, block in enumerate(blocks):
        if block["BlockType"] == "LINE":
            text =  block["Text"]
            if "ago" in text:
                user = text.split(" ")[0]
                textIdList.append(user)
            else:
                if not text.isnumeric():
                    textIdList.append(text)
                if len(textIdList) == 3:
                    break
    idDict = {"File": {filename.split(".")[0]: {"TaskId" : {textIdList[0]: "".join(textIdList[1:])}}}}
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




