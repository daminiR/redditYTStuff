import xml.etree.ElementTree as ET
import sys
import os

def get_new_mark(markType="comment", storyNumber=None):
    #create element and set attributes
    mark = ET.Element('mark')
    if markType == "comment":
        mark.attrib['name'] = "COMMENT"

    if markType == "story":
        mark.attrib['name'] = "STORY" + str(storyNumber)
    return mark

def get_new_break():
    #create element and set attributes
    pause = ET.Element('break')
    pause.attrib['time'] = "0.5s"
    return pause

def xmlTreeModifier(redditFolder):
    print("processing xml ... ")
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    xml_file = 'ssml.xml'

    tree = ET.parse(redditFolder + '/ssml/original/' + xml_file, parser=parser)
    root = tree.getroot()
    allTags = root.findall("./amazon/")
    coef = 0
    for index, child in enumerate(allTags):
        if child.text:
            # if story or comment
            breakElement = get_new_break()
            if "ago" in child.text:
                commentElement = get_new_mark(markType="comment")
                root.getchildren()[0].insert(index + coef, breakElement)
                root.getchildren()[0].insert(index + coef, commentElement)
                root.getchildren()[0].insert(index + coef, breakElement)
                coef  += 3

            if "STORY" in child.text:
                storyNumber = child.text.replace(' ', '').split("STORY")[1]
                storyElement= get_new_mark(markType="story", storyNumber=storyNumber)
                root.getchildren()[0].insert(index + coef, breakElement)
                root.getchildren()[0].insert(index + coef, storyElement)
                root.getchildren()[0].insert(index + coef, breakElement)
                coef  += 3
    amazon_val = root.findall("./")
    amazon_val[0].tag = "amazon:domain"
    new_xml_tree_string = ET.tostring(tree.getroot())
    with open(redditFolder + '/' 'ssml/edited/'+ xml_file.split('.')[0] + '_processed.xml', "wb+") as f:
            f.write(new_xml_tree_string)
