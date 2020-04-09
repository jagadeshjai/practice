import xml.etree.ElementTree as ET
myTree = ET.parse("components_chromium_strings.grd")
root = myTree.getroot()
# message = root.iterfind("message")
# print(message)
# for child in root.iter("message"):
#     print(child.text)
# print("\n-----------------------------------------\n")
# for child in root.iter("message"):
#     print(child.attrib["name"])

for x in root.itertextjai():
    print(x+" --> ")


