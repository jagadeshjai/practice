from xml.dom import minidom
import os
import json


def stringScan():
    with open("duplicate.xml", "r") as file:
        fileContents = file.read()
    for string in defaultString:
        count = fileContents.count(string)
        defaultString[string] += count
    print(defaultString)


'''
Get the text values from the given node and its child nodes
'''


def getText(nodelist):
    rc = []
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.nodeValue.replace('\n', '').replace('"', ''))
    return ''.join(rc)


# Driver code
defaultString = {
    "Chromium": 0,
    "Chrome": 0,
    "Google": 0
}
# dom = minidom.parse("components_chromium_strings.grd")
# message = dom.getElementsByTagName("message")

# # Creating a text file to store IDS and its equivalent text values as json

# textFile = open("changes.json", "w")
# textFile.write("{\n")
# for msg in message:
#     # textFile.write((msg.attributes['name'].value + " : "+ "".join(t.nodeValue for t in msg.childNodes if t.nodeType == t.TEXT_NODE)).encode('utf-8'))
#     textFile.write(("\""+msg.attributes['name'].value+"\"" +
#                     " : " + "\"" + getText(msg) + "\",\n").encode("utf-8"))

# textFile.seek(-2, os.SEEK_END)
# textFile.truncate()
# textFile.write("\n}")
# textFile.close()

# # Get the file content from text file as dict

# textFile = open("changes.json", 'r')
# fileContent = (textFile.read())
# # fileContent = fileContent.replace('\n', '')
# jsonDict = json.loads(fileContent)
# print(jsonDict["IDS_DEPRECATED_FEATURES_RELAUNCH_NOTICE"])
# textFile.close()

stringScan()
