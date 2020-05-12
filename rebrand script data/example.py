import xml.etree.ElementTree as ET
STRING = """<?xml version="1.0" encoding="utf-8"?>
<!--
This file contains definitions of resources that will be translated for each
locale.  The variables is_win, is_macosx, is_linux, and is_posix are available
for making strings OS specific.  Other platform defines such as use_titlecase
are declared in tools/grit/grit_rule.gni.
-->
<fruits name = "Jai">
   <item color="red">
       <name>apple</name>
       <count>1</count>
   </item>
   <item color="yellow">
       <name>banana</name>
       <count>2</count>
   </item>
</fruits>"""
tree = ET.parse("new.xml")
root = tree.getroot()
print(root.find("item"))
# for elem in root.iter("item"):
#     for child in list(elem):
#         elem.remove(child)
for elem in root.iter("item"):
    elem.clear()
ET.dump(root)

# tree.write("new1.xml", xml_declaration=True, encoding='utf-8',method="xml")

