import os.path
import re
import shutil
from xml.dom import minidom

sourcecDirectory = os.path.join(os.getcwd(),"src")

chromiumStringsPath = os.path.join(sourcecDirectory, 'chrome', 'app', 'chromium_strings.grd')
primeumStringsPath = os.path.join(sourcecDirectory, 'primeum', 'app', 'chromium_strings.grd')

#chromiumSettingsPartPath = os.path.join(sourcecDirectory, 'chrome', 'app', 'settings_chromium_strings.grdp')
#primeumSettingsPartPath = os.path.join(sourcecDirectory, 'primeum', 'app', 'settings_chromium_strings.grdp')

chromiumComponentsChromiumStringsPath = os.path.join(sourcecDirectory, 'components', 'components_chromium_strings.grd')
primeumComponentsPrimeumtringsPath = os.path.join(sourcecDirectory, 'primeum', 'components', 'components_chromium_strings.grd')

chromiumComponentsStringsPath = os.path.join(sourcecDirectory, 'components', 'components_strings.grd')
primeumComponentsStringsPath = os.path.join(sourcecDirectory, 'primeum', 'components', 'components_strings.grd')

chromiumGeneratedResourcesPath = os.path.join(sourcecDirectory, 'chrome', 'app', 'generated_resources.grd')
primeumGeneratedResourcesPath = os.path.join(sourcecDirectory, 'primeum', 'app', 'generated_resources.grd')


def grdpsPartsfromgrd(chromiumPath):
    grdContents = minidom.parse(chromiumPath)
    partsContents = grdContents.getElementsByTagName('part')
    parts = []
    for part in partsContents:
        parts.append(part.attributes['file'].value)
    return parts
'''
Helper function to auto generate the mapping
'''
def autoGenerateMapping(chromiumPath , primeumPath ):
    if( os.path.exists(chromiumPath) != True ):
        print ("File not present :"+chromiumPath)
        exit()
    grdps = grdpsPartsfromgrd(chromiumPath)
    chromiumToPrimeumMapping[chromiumPath] = primeumPath
    if ( len(grdps) > 0 ) :
        chromiumDirectoryPath = os.path.dirname(chromiumPath)
        primeumDirectoryPath = os.path.dirname(primeumPath)
        for grdp in grdps:
            chromiumToPrimeumMapping[os.path.join(chromiumDirectoryPath,grdp)] = os.path.join(primeumDirectoryPath,grdp)

'''
Global variable which handles the mapping of primeum to chromium
'''
chromiumToPrimeumMapping = {
}

'''
Replacing the Chromium to primeum by simply reading the passed file map
'''

defaultReplacements = [
  [re.compile(r"Chrome Web Store"), 'Web Store'],
  [re.compile(r"The Chromium Authors\n"), 'Zoho Authors\n'],
  [re.compile(r"The Chromium Authors. All rights reserved"), 'The Zoho Authors. All rights reserved.'],
  [re.compile(r"Google Chrome"), 'Primeum'],
  [re.compile(r"Chromium"), 'Primeum'],
  [re.compile(r"Chrome"), 'Primeum'],
  [re.compile(r"Google LLC. All rights reserved."), 'The Zoho Authors. All rights reserved.'],
  [re.compile(r"Google"), 'Primeum'],
]

def copyRebranded() :
    chromeComponentsDir = os.path.join(sourcecDirectory, 'components')
    primeumComponentsDir = os.path.join(sourcecDirectory, 'primeum','components')
    chromeAppDir = os.path.join(sourcecDirectory, 'chrome', 'app')
    primeumAppDir = os.path.join(sourcecDirectory, 'primeum','app')
    #TODO copy the files with timestamp
    for key in chromiumToPrimeumMapping:
        shutil.copy(chromiumToPrimeumMapping[key],key)
        print ("file "+chromiumToPrimeumMapping[key]+" copied to "+key )
    



def replaceChromiumToPrimeum():
    autoGenerateMapping(chromiumComponentsStringsPath,primeumComponentsStringsPath)
    autoGenerateMapping(chromiumStringsPath,primeumStringsPath)
    autoGenerateMapping(chromiumComponentsChromiumStringsPath,primeumComponentsPrimeumtringsPath)
    autoGenerateMapping(chromiumGeneratedResourcesPath,primeumGeneratedResourcesPath)

    for key in chromiumToPrimeumMapping :
        sourcefilefd = open(key, "r")
        destinationFilefd = open(chromiumToPrimeumMapping.get(key), "w" )
        fileContents = sourcefilefd.read()
        for replacement in defaultReplacements:
            fileContents = replacement[0].sub(replacement[1],fileContents)
        
        destinationFilefd.write(fileContents)
        
        sourcefilefd.close()
        destinationFilefd.close()

    copyRebranded()

replaceChromiumToPrimeum()

