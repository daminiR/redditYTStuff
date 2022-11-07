import os
from xml.dom import minidom
import sys

if __name__ == "__main__":
    rootDir = sys.argv[1]
    root = minidom.Document()
    xml = root.createElement('speak')
    root.appendChild(xml)
    awsChild = root.createElement('amazon')
    awsChild.setAttribute('name', "news")

    breakChild = root.createElement('break')
    breakChild.setAttribute('time', "1s")
    awsChild.appendChild(breakChild)
    awsChild.appendChild(breakChild)
    xml.appendChild(awsChild)
    xml_str = root.toprettyxml(indent="\t")
    with open(os.path.join(rootDir, 'ssml/original/ssml.xml'), "w") as f:
        f.write(xml_str)
    f.close()

