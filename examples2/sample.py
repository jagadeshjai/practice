import os.path
from xml.dom import minidom
import re

# sourceDirectory = os.path.join(os.getcwd(),"src")
# chromiumStringsPath = os.path.join(sourceDirectory, 'chrome', 'app', 'chromium_strings.grd')
# chromiumComponentsChromiumStringsPath = os.path.join(sourceDirectory, 'components', 'components_chromium_strings.grd')
# chromiumComponentsStringsPath = os.path.join(sourceDirectory, 'components', 'components_strings.grd')
# chromiumGeneratedResourcesPath = os.path.join(sourceDirectory, 'chrome', 'app', 'generated_resources.grd')

# initialStringsPath = [
#     chromiumStringsPath,
#     chromiumComponentsChromiumStringsPath,
#     chromiumComponentsStringsPath,
#     chromiumGeneratedResourcesPath
#     ]

initialStringsPath = [
    "components_chromium_strings.grd"
    ]

'''
Global variable for the files to be changed
'''

stringFilesPath = [

]


def grdpsPartsfromgrd(chromiumPath):
    grdContents = minidom.parse(chromiumPath)
    partsContents = grdContents.getElementsByTagName('part')
    parts = []
    for part in partsContents:
        parts.append(part.attributes['file'].value)
    return parts


def autoGenerateMapping(chromiumPath):
    if( os.path.exists(chromiumPath) != True ):
        print ("File not present :"+chromiumPath)
        exit()
    grdps = grdpsPartsfromgrd(chromiumPath)
    stringFilesPath.append(chromiumPath)
    if ( len(grdps) > 0 ) :
        chromiumDirectoryPath = os.path.dirname(chromiumPath)
        for grdp in grdps:
            stringFilePath.append(os.path.join(chromiumDirectoryPath,grdp))

"""
Method to scan string from the given list
"""

def stringScan():
    for path in initialStringsPath:
        autoGenerateMapping(path)

    for value in stringFilesPath:
        with open(value,"r") as file:
            fileContents =  file.read()
            for string in defaultString:
                count = fileContents.count(string)
                defaultString[string] = defaultString[string] + count 
    print(defaultString)

defaultString = {
    "chromium" : 0,
    "chrome" : 0,
    "Chromium":0
}

stringScan()