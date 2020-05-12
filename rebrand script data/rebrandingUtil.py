#!/usr/bin/python3
"""
Before using this script backup "src/components" and "src/chrome/app" directory

Uses of this script:

first create a duplicate file called duplicate_original by passing an argument '-cdx'

 And review that file and save it as duplicate_reviewed
then once its reviewed pass an argument '-atochromium' to change the string files in "src/components" and "src/chrome/app"

If higher version of chromium cloned then check for new nodes in strings file in chromium by comparing with duplicate_orginal file(previous version)
by passing an argument '-check' which create a file called to_be_reviewed that stores new elements
And once its reviewed pass the argument '-atoduplicate' that appends the new nodes to duplicate_reviwed file(previous version's file)
Now you can use '-atochromium' to change the string files in "src/components" and "src/chrome/app"

"""

import json
import os
import sys
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom
from distutils.dir_util import copy_tree


class ConsoleStyle():
    """ Styles for terminal output. """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def display_flags():
    """
    Method to print the function exists
    """
    print(ConsoleStyle.YELLOW + 'Select the method to invoke.' + ConsoleStyle.RESET)
    print("""
    -backup       : to backup string files ("src/components" and "src/chrome/app")\n
    -cdx          : to create duplicate file from existing chromium string files\n
    -append       : to append the new strings to reviewed data file\n
    -rebrand      : to change the string files in chromium from duplicate_reviewed file\n
    -check        : to store the new elements present in updated string files\n""")


def log(msg=None):
    """
    Function to set the status of the script
    """
    if (msg is not None):
        with open(".strings_log", 'w') as log_file:
            log_file.write(msg)
            return None
    else:
        with open(".strings_log", 'r') as log_file:
            return log_file.read()


def _display_check_steps():

    ready = input("Are you ready to review now (yes/no) :  ")
    if(ready.lower() == "yes"):
        if(input("If you reviwed type 'yes' to continue or 'no' for later (yes/no) :  ").lower() == "yes"):
            print("Appendind new nodes in reviewed_data...\n")
            append_reviewed_elements()
            print("\nReplacing strings from reviewed_data...\n")
            replace_reviewed_xml()
            print("\nRebranding of strings" + ConsoleStyle.GREEN +
                  " DONE..." + ConsoleStyle.RESET)
            log("Done")
        else:
            log("Not_reviewed")
            print("\nContinue Later...")
    else:
        log("Not_reviewed")
        print("\nContinue Later...")


def to_backup_strings():
    """
    Function to copy "src/components" and "src/chrome/app" to backup_strings dir in chromium/src/
    """
    subprocess.run(['mkdir', os.path.join(
        SOURCE_DIRECTORY, 'backup_strings')])
    subprocess.run(['cp', '-a', os.path.join(
        SOURCE_DIRECTORY, 'components'), os.path.join(
        SOURCE_DIRECTORY, 'backup_strings')])
    subprocess.run(['cp', '-a', os.path.join(
        SOURCE_DIRECTORY, 'chrome', 'app'), os.path.join(
            SOURCE_DIRECTORY, 'backup_strings')])


def _grdps_parts_from_grd(chromium_path):
    """
    Helper function to grdps from part tag
    """
    grd_contents = minidom.parse(chromium_path)
    parts_contents = grd_contents.getElementsByTagName('part')
    parts = []
    for part in parts_contents:
        parts.append(part.attributes['file'].value)
    return parts


def _list_of_files_path(chromium_path):
    """
    Helper function to get required files path
    """
    if(os.path.exists(chromium_path) is not True):
        print("File not present :"+chromium_path)
        sys.exit()
    grdps = _grdps_parts_from_grd(chromium_path)
    STRINGS_FILES_PATHS.append(chromium_path)
    if (len(grdps) > 0):
        chromium_directory_path = os.path.dirname(chromium_path)
        for grdp in grdps:
            STRINGS_FILES_PATHS.append(
                os.path.join(chromium_directory_path, grdp))


def _strings_count(file_name):
    """
    Method to get the string count from the strings files
    """
    with open(file_name, "r") as file:
        file_contents = file.read()
        for string in DEFAULT_STRINGS:
            count = file_contents.count(string)
            DEFAULT_STRINGS[string] += count
    print("\n" + DEFAULT_STRINGS.__str__())


def get_text(nodelist):
    '''
    Get the text values from the given node and its child nodes
    '''
    rc = []
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.nodeValue.replace('\n', '').replace(
                '"', ''))
    return ''.join(rc)


def create_json():
    '''
    Creating a Json file from message tags
    '''
    for path in INITIAL_STRINGS_PATH:
        _list_of_files_path(path)
    text_file = open("changes.json", "w")
    text_file.write("{\n")
    text_file.close()
    for value in STRINGS_FILES_PATHS:
        with open(value, "r") as file:
            dom = minidom.parse(file)
        message = dom.getElementsByTagName("message")

        # Creating a text file to store IDS and its equivalent text values as json

        text_file = open("changes.json", "a")
        for msg in message:
            text_file.write(
                ("\""+msg.attributes['name'].value+"\"" + " : " + "\"" + get_text(msg) + "\",\n").encode("utf-8"))
        text_file.close()
    with open("changes.json", "r+") as text_file:
        text_file.seek(-2, os.SEEK_END)
        text_file.truncate()
        text_file.write("\n}")

    # Get the file content from json file as dict

    text_file = open("changes.json", 'r')
    file_content = (text_file.read())
    json_dict = json.loads(file_content.replace("\share", '/share'))
    text_file.close()
    print("createJson executed")


def create_duplicate_xml():
    """
    Creating duplicate xml file which cantains message tag in each file inside fileName tag
    """
    for path in INITIAL_STRINGS_PATH:
        _list_of_files_path(path)
    duplicate_tag = ET.Element("duplicate")
    for value in STRINGS_FILES_PATHS:
        tree = ET.parse(value)
        root = tree.getroot()
        value = value.replace(os.path.join(
            SOURCE_DIRECTORY, 'chrome', 'app')+'/', '').replace(os.path.join(
                SOURCE_DIRECTORY, 'components')+'/', '')
        file_name_tag = ET.SubElement(duplicate_tag, value)
        messages = 0
        for msg in root.iter("messages"):
            if msg is not None:
                messages = 1
        if messages:
            file_name_tag.append(msg)
        else:
            file_name_tag.append(root)
    with open(os.path.join(
            SOURCE_DIRECTORY, 'rebranding', 'strings', 'duplicate_orginal.xml'), 'w') as duplicat_file:
        duplicate_xml = ET.tostring(duplicate_tag)
        duplicat_file.write(duplicate_xml)
    print("Duplicate string file is created from chromium strings files")


# TODO add a comment in every file

def replace_reviewed_xml():
    """
    changes from duplicate xml file is updated to resp. files
    """
    for path in INITIAL_STRINGS_PATH:
        _list_of_files_path(path)
    # duplicate_file = ET.parse(os.path.join(
    #     SOURCE_DIRECTORY, 'rebranding', 'strings', 'duplicate_reviewed.xml'))
    duplicate_file = ET.parse("duplicate3.xml")
    for value in STRINGS_FILES_PATHS:
        tree = ET.parse(value)
        root = tree.getroot()
        file_name = value.replace(os.path.join(
            SOURCE_DIRECTORY, 'chrome', 'app')+'/', '').replace(os.path.join(
                SOURCE_DIRECTORY, 'components')+'/', '')
        curr_file = "messages" if duplicate_file.find(
            file_name).find("messages") is not None else "grit-part"
        release = root.find("release")
        if release is not None:
            for elem in root.iter("release"):
                for child in elem:
                    elem.remove(child)
            release.append(duplicate_file.find(file_name).find(curr_file))
        else:
            root.clear()
            root.extend(duplicate_file.find(file_name).find(curr_file))
        comment = ET.Comment(
            ' \nThis file is generated by rebrandingUtil.py script, backup files are stored in backup_string directory in chromium/src/ and don\'t modify this manually\n')
        root.insert(0, comment)

        tree.write(value, xml_declaration=True, encoding='utf-8', method="xml")
    print("Chromium string files are changed from duplicate_reviewed file")


def check_for_new_elements():
    """
    check if the file has new elements(compare with duplicate.xml) and store it under file_name as parent node
    """
    for path in INITIAL_STRINGS_PATH:
        _list_of_files_path(path)
    # duplicate_file = ET.parse(os.path.join(
    #     SOURCE_DIRECTORY, 'rebranding', 'strings', 'duplicate_orginal.xml'))
    duplicate_file = ET.parse("duplicate3.xml")
    new_elements = ET.Element("new_elements")
    count = 0  # count variable to get the count of new elements
    parts = 0
    for value in STRINGS_FILES_PATHS:
        tree = ET.parse(value)
        root = tree.getroot()
        file_name = value.replace(os.path.join(
            SOURCE_DIRECTORY, 'chrome', 'app')+'/', '').replace(os.path.join(
                SOURCE_DIRECTORY, 'components')+'/', '')

        # Below code converts the fileName element object to string in xml format

        curr_duplicate_file_content = ET.tostring(
            list(duplicate_file.find(file_name))[0])
        release = root.find("release")
        if release is not None:
            curr_actual_file_content = release.find("messages")
        else:
            curr_actual_file_content = root
        for content in list(curr_actual_file_content):
            if ET.tostring(content).rstrip() not in curr_duplicate_file_content:

                # Below block of code check whether there is new grdp file included if exist then add it to to_be_reviwed file

                if(content.tag == "part"):
                    parts += 1
                    # print("\n" + ET.tostring(content).decode())
                    file_name_tag = ET.SubElement(
                        new_elements, content.attrib['file'])
                    grit_tree = ET.parse(value.replace(
                        file_name, content.attrib['file']))
                    grit_root = grit_tree.getroot()
                    file_name_tag.append(grit_root)
                else:
                    count += 1
                file_name_tag = ET.SubElement(new_elements, file_name)
                file_name_tag.append(content)

    # with open(os.path.join(
    #         SOURCE_DIRECTORY, 'rebranding', 'strings', 'to_be_reviewed.xml'), 'w') as review_file:
    with open("to_be_reviwed.xml", "wb") as review_file:
        review_xml = ET.tostring(new_elements)
        review_file.write(review_xml)

    print("\n  " + ConsoleStyle.GREEN + parts.__str__() +
          ConsoleStyle.RESET + " New part file are included in chromium current version")
    print("\n  " + ConsoleStyle.GREEN + count.__str__() + ConsoleStyle.RESET +
          " New child nodes found, kindly check to_be_reviewed.xml\n")
    _strings_count("to_be_reviwed.xml")


def append_reviewed_elements():
    """
    Method to append the elements from ty.attribhe to_be_reviwed file after its reviwed to duplicateData file
    """

    # duplicate_data_file = ET.parse(os.path.join(
    #     SOURCE_DIRECTORY, 'rebranding', 'strings', 'duplicate_reviewed.xml'))
    # reviwed_file = ET.parse(os.path.join(
    #     SOURCE_DIRECTORY, 'rebranding', 'strings', 'to_be_reviewed.xml'))

    duplicate_data_file = ET.parse("duplicate4.xml")
    root_of_duplicate = duplicate_data_file.getroot()
    reviwed_file = ET.parse("to_be_reviwed.xml")
    root_of_reviwed = reviwed_file.getroot()
    for elem in list(root_of_reviwed):
        # duplicate_data_file.find(elem.tag).extend(elem)

        for rev_1 in list(root_of_reviwed.find(elem.tag)):
            for dup_1 in list(root_of_duplicate.find(elem.tag))[0]:
                if(rev_1.tag == "if" and dup_1.tag == "if"):
                    if(rev_1.attrib['expr'] == dup_1.attrib['expr']):
                        for rev_2 in list(rev_1):
                            for dup_2 in list(dup_1):
                                if(rev_2.attrib['name'] == dup_2.attrib['name']):
                                    dup_1.clear()
                                    root_of_duplicate.find(
                                        elem.tag).extend(elem)
                                    print("If Excuted")
                elif(rev_1.tag == "message" and dup_1.tag == "message"):
                    if(rev_1.attrib['name'] == dup_1.attrib['name']):
                        dup_1.clear()
                        duplicate_data_file.find(elem.tag).extend(elem)
                        print("Else Excuted")

    duplicate_data_file.write("after_appending_reviwed.xml")
    # duplicate_data_file.write(os.path.join(
    #     SOURCE_DIRECTORY, 'rebranding', 'strings', 'after_appending_reviwed.xml'))
    # print("Created " + os.path.join(
    #     SOURCE_DIRECTORY, 'rebranding', 'strings', 'after_appending_reviwed.xml') + "file")


# Driver Program

SOURCE_DIRECTORY = os.path.join(os.getcwd(), "src")
CHROMIUM_STRINGS_PATH = os.path.join(
    SOURCE_DIRECTORY, 'chrome', 'app', 'chromium_strings.grd')
CHROMIUM_COMPONENTS_CHROMIUM_STRINGS_PATH = os.path.join(
    SOURCE_DIRECTORY, 'components', 'components_chromium_strings.grd')
CHROMIUM_COMPONENTS_STRINGS_PATH = os.path.join(
    SOURCE_DIRECTORY, 'components', 'components_strings.grd')
CHROMIUM_GENERATED_RESOURCES_PATH = os.path.join(
    SOURCE_DIRECTORY, 'chrome', 'app', 'generated_resources.grd')

INITIAL_STRINGS_PATH = [
    CHROMIUM_STRINGS_PATH,
    CHROMIUM_COMPONENTS_CHROMIUM_STRINGS_PATH,
    CHROMIUM_COMPONENTS_STRINGS_PATH,
    CHROMIUM_GENERATED_RESOURCES_PATH
]

# Image directories

chromiumDir = os.path.join(SOURCE_DIRECTORY, 'chrome')
primeumDir = os.path.join(SOURCE_DIRECTORY, 'primeum')
primeumImagesDir = [
    [os.path.join(chromiumDir, 'app', 'theme', 'chromium'),
     os.path.join(primeumDir, 'app', 'theme', 'chromium')],
    [os.path.join(chromiumDir, 'app', "theme", "default_100_percent", 'chromium'), os.path.join(
        primeumDir, 'app', "theme", "default_100_percent", "chromium")],
    [os.path.join(chromiumDir, 'app', "theme", "default_200_percent", 'chromium'), os.path.join(
        primeumDir, 'app', "theme", "default_200_percent", "chromium")],
    [os.path.join(chromiumDir, 'app', "vector_icons", 'chromium'),
     os.path.join(primeumDir, 'app', "vector_icons", "chromium")],
    [os.path.join(SOURCE_DIRECTORY, 'components', 'omnibox', 'browser', 'vector_icons'),
     os.path.join(primeumDir, 'components', 'omnibox', 'browser', 'vector_icons')],
    [os.path.join(SOURCE_DIRECTORY, 'ui', 'message_center', 'vector_icons'),
     os.path.join(primeumDir, 'ui', 'message_center', 'vector_icons')]
]

for primeumImageMapList in primeumImagesDir:
    print("Images copied List")
    print(copy_tree(primeumImageMapList[1],primeumImageMapList[0]))

DEFAULT_STRINGS = {
    "Chromium": 0,
    "Chrome": 0,
    "Google": 0
}

"""
Global variable for the files to be changed
"""
STRINGS_FILES_PATHS = [

]

'''
Calling the function by the given aruguments
'''
# try:
#     sys.argv[1]
# except IndexError:
#     display_flags()
#     sys.exit()

# if(sys.argv[1] == "-backup"):
#     to_backup_strings()
# elif(sys.argv[1] == "-cdx"):
#     create_duplicate_xml()
# elif(sys.argv[1] == "-check"):
#     if(log() == "Not_reviewed"):
#         print("Already checked and 'to_be_reviewed' file created\n")
#         _display_check_steps()
#         sys.exit()
#     check_for_new_elements()
#     _display_check_steps()
# elif(sys.argv[1] == "-rebrand"):
#     replace_reviewed_xml()
# elif(sys.argv[1] == "-append"):
#     append_reviewed_elements()
# else:
#     print("Invalid arugument!\n")
#     display_flags()
