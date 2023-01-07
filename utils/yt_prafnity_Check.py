import re
import string

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def checkYoutubeProfanity(text):
    with open('./assets/profane_google_list.txt', 'r')  as file:
        lines = file.readlines()
        for profane_term in lines:
            newText = text.translate(str.maketrans('', '', string.punctuation))
            if findWholeWord(profane_term)(newText) != None:
                # print("could be banned by google!")
                # print(profane_term)
                # print(text)
                return True
        return False


