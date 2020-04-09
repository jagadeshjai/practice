from xml.dom import minidom
import ast
dom = minidom.parse("components_chromium_strings.grd")

#Get the text values from the given node and its child nodes

def getText(nodelist):
    rc = []
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.nodeValue)
    return ''.join(rc)

message = dom.getElementsByTagName("message")

#Creating a text file to store IDS and its equivalent text values

textFile = open("changes.json","w")
textFile.write("{")
for msg in message:
    # textFile.write((msg.attributes['name'].value + " : "+ "".join(t.nodeValue for t in msg.childNodes if t.nodeType == t.TEXT_NODE)).encode('utf-8'))
    textFile.write(("\""+msg.attributes['name'].value+"\"" + " : " + "\"" + getText(msg) + "\",").encode('utf-8'))
textFile.write("}")
textFile.close()


#Get the file content from text file as dict

textFile = open("changes.json","r")
fileContent = ast.literal_eval(textFile.read())
print(fileContent)
textFile.close()