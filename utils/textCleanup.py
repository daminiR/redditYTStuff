import json
import re
from profanity_check import predict, predict_prob

def checkProfane(text):
    sentences = text.split(" ")
    isProfane = predict(sentences)
    if any(isProfane):
        # print(text)
        return True
    else:
        return False

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    text = re.sub(emoj, "", data)
    if text == "" or text =="\n":
        return ""
    else:
        return text


def convertToBox(x1, y1, x2, y2):
    return [int((x2 + x1)/2 ), int((y2 + y1)/2), int(x2 - x1), int(y2 - y1)]

def redo():
    inputFile = "/Users/daminirijhwani/redditYTStuff/assets/abreviations.json"
    outFile = "/Users/daminirijhwani/redditYTStuff/assets/abreviations_new.json"
    with open(inputFile, 'r') as input, open(outFile, 'w+') as output:
        lines = input.readlines()
        for line in lines:
            line = re.sub('\"', ' \" ', line)
            output.write(line)

def cleanAbreviations(new):
    inputFile = "/Users/daminirijhwani/redditYTStuff/assets/abreviations_new.json"
    with open(inputFile, 'r') as h:
        lines = json.load(h)["abreviations"]
        for k, v in lines.items():
            new = new.replace(k, v)
            new = new.replace(k.upper(), v)
        return new

def redditAcronyms(line):
    new = line.replace("AITA", "Am I The Asshole")
    new = new.replace("AMA", "Ask Me Anything")
    new = new.replace("AMAA", " Ask Me Almost Anything")
    new = new.replace("DAE", "Does Anyone Else")
    new = new.replace("ELI5", "Explain like I'm 5")
    new = new.replace("FTA", "From The Article")
    new = new.replace("FTFY", "Fixed That For You")
    new = new.replace("GW", "Gone Wild")
    new = new.replace("IAMA", "I Am A")
    new = new.replace("IMO", "In My Opinion")
    new = new.replace("IMHO", "In My Humble (Honest) Opinion")
    new = new.replace("IIRC", "If I Recall Correctly")
    new = new.replace("ITT", "In This Thread")
    new = new.replace("MIC", "More In Comments")
    new = new.replace("OP", "O.P")
    new = new.replace("RTFA", "Read the fucking article")
    new = new.replace("SRD", "Subreddit drama")
    new = new.replace("TIL", "Today, I learned")
    new = new.replace("WIP", "Work in progress")
    new = new.replace("NTA", "Not the Asshole")
    new = new.replace("YTA", "You're the Asshole")
    new = new.replace("WIBTA", "Would I be the asshole")
    new = new.replace("NAH", "no assholes here")
    new = new.replace("ESH", "everyone sucks here")
    new = new.replace("WIBTA", "Would I be the asshole")
    new = new.replace("WTF", "W.T.F")
    new = new.replace("CMV", "Change my view")
    new = new.replace("IANAD", "I am not a doctor")
    new = new.replace("IANAL", "I am not a lawyer")
    new = new.replace("MRW", "My reaction when")
    new = new.replace("MFW", "My face when")
    new = new.replace("MFW", "Public service announcement")
    new = new.replace("YSK", "You should know")
    new = new.replace("TL;DR ", "Too long; Didn’t read")
    new = new.replace("OC", "O.C")
    new = new.replace("SRS", "Shit Reddit Says")
    new = new.replace("SO", "Significant Other")
    new = new.replace("DM;HS", "Doesnt Matter, Had Sex")
    new = new.replace("IRL", "In Real Life")
    new = new.replace("GTFO", "Get The Fuck Out")
    new = new.replace("YMMV", "your mileage may vary")
    new = new.replace("SMH", "Shaking my head")
    new = new.replace("LSHMSFOAIDMT", "Laughing So Hard My Sombrero Falls Off and I Drop My Taco")
    # bad words
    new = new.replace("Fuck", "f-")
    new = new.replace("fuck", "f-")
    new = new.replace("asshole", "ahole")
    new = new.replace("asshole", "ahole")
    return new
def cleanTTS(line):
    gibrish = [
        "Posts\n",
        "Wiki\n",
        "Best of AskReddit\n",
        "r/AskReddit\n",
        "Search Reddit\n",
        "r/AskReddit ⌧\n",
        "� Advertise\n",
        "Gilded\n",
        "Sort By: Best\n",
        "Related Subreddits\n",
        "Secret\n",
        "� Award\n",
        "� Share\n",
        "� Save\n",
        "This thread is archived\n",
        "New comments cannot be posted and votes cannot be cast\n",
        "�\n"
    ]
    regex_user= r'Comment deleted by user · \d{1,3} (min.|day|days|mo.|yr.|hr.) ago(.*)'
    regex_hidden_user = r'· \d{1,3} (min.|day|days|mo.|yr.|hr.) ago(.*)$'
    regex_comments=r'^\d{1,5}.\dk$'
    regex_more=r'\d{1, 4} More$'
    plus=r'\+\d+\n$'
    new = line.replace("\"", "")
    new = new.replace("&", "&amp;")
    new = new.replace("\'", "&apos;")
    new = new.replace("<", "&lt;")
    new = new.replace(">", "&gt;")
    if "hardlyHuman23" in new:
        new = ""
    for gib in gibrish:
        new = new.replace(gib, "")
    # regex stuff
    deleted_found = re.search(regex_user,new)
    if re.search(plus,new):
        new = ""
    if deleted_found:
        new = re.sub(regex_user,  "", new)
    if re.search(regex_comments,new):
        new = ""
    if re.search(regex_more,new):
        new = ""
    if re.search(regex_hidden_user,new):
        new = ""
    if "http" in new:
        new = ""
    return new

def clean(blocks):
    regex_  = r'^\d+\n$'
    regex_2  = r'^\d+ & \d+ More\n$'
    new_blocks = []
    for block in blocks:
        if not re.search(regex_, block[4]) and not re.search(regex_2, block[4]):
            new_blocks.append(block)
    return new_blocks

