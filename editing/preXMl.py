import os
from xml.dom import minidom
import sys


if __name__ == "__main__":
    rootDir = sys.argv[1]
    root = minidom.Document()
    xml = root.createElement('speak')
    root.appendChild(xml)
    breakChild = root.createElement('break')
    breakChild.setAttribute('time', "0.5s")
    xml.appendChild(breakChild)
    xml_str = root.toprettyxml(indent="\t")
    with open(os.path.join(rootDir, 'ssml/original/ssml.xml'), "w") as f:
        f.write(xml_str)
    f.close()

