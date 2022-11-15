import json

redditFolder="TTSData/ytData/AskReddit/reddit_yt_3"
with open(redditFolder + "/sync/screenshotTimestamps.json") as f:
        timestamps = json.load(f)["ImageTimeStamps"]
        for timestamp in timestamps:
            if "STORY" not in timestamp["Mark Sentence"]:
                confidence = timestamp["Confidence"]
                if confidence < 0.5:
                        print("////////////////////////////////////////////////")
                        print(timestamp["Mark Sentence"])
                        print(timestamp["TaskId"])

