import xml.etree.ElementTree as ET
import sys
import os
## add first break pause
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
# do it with pointers??


def xmlTreeModifier(rootDir):
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    xml_file = 'ssml.xml'

    tree = ET.parse(rootDir + '/' + xml_file, parser=parser)
    root = tree.getroot()
    allTags = root.findall("./{aws}domain/")
    coef = 0
    for index, child in enumerate(allTags):
        # if '<function Comment at' in child.tag:
        if child.text:
            # if story or comment
            breakElement = get_new_break()
            if "days ago" in child.text:
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

    new_xml_tree_string = ET.tostring(tree.getroot())
    with open(xml_dir + '/' + xml_file + '_processed.xml', "wb") as f:
            f.write(new_xml_tree_string)

