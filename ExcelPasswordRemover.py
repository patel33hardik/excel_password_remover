import os
import shutil
import zipfile
import re
import traceback


def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def printGreen(text):
    print_colored(text, '32')

def printRed(text):
    print_colored(text, '31')

def createFolder(foldername):
    try:
        #Create Directory
        os.mkdir(foldername)
        print("Directory " , foldername , "created! ")
    except FileExistsError:
        print("Directory" , foldername , "already exists!")

def reppydirs(pyimport, pyexport):
    # Get current workdir
    global reppytemp, workindir, reppyimport, reppyexport
    workindir = os.getcwd()
    # create Required Folders
    reppyimport = os.path.join(workindir, pyimport)
    reppytemp = os.path.join(workindir, 'temp')
    reppyexport = os.path.join(workindir, pyexport)

    createFolder(reppyimport)
    createFolder(reppytemp)
    createFolder(reppyexport)



# Replaces the Password String inside the XML Sheets
def findPasswordLine(inputSource):
    print('--locals-{}--'.format(locals()))

    # Read the content of the input file
    with open(inputSource, "r", encoding="utf-8") as input_file:
        input_content = input_file.read()

    # Replace the string using regex
    modified_content = re.sub('<sheetProtection.*?.>', '', input_content)

    # Write the modified content back to the input file
    with open(inputSource, "w", encoding="utf-8") as input_file:
        input_file.write(modified_content)


def create_zip_from_directory(source_directory, zip_path, new_zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_directory)
                zipf.write(file_path, arcname=arcname)

    shutil.copy(zip_path, new_zip_path)

def cleanupTemp(tempfolder):
    print(f'Deleting folder {tempfolder} !')
    try:
        shutil.rmtree(tempfolder)
    except:
        printRed(f'Could not delete {tempfolder} folder. Please delete manually!')

def main(rimport,rtemp,rexport):
    print(locals())
    listOfFile = os.listdir(rimport)
    dst_exp_dir = None
    for file in listOfFile:
        # Copy file to work with
        if '.xlsx' not in file:
            continue
        src_dir = os.path.join(rimport, file)
        dst_temp_dir = os.path.join(rtemp, f'temp_{file}')
        dst_exp_dir = os.path.join(rexport, f'UnProtected{file}')
        shutil.copy(src_dir,dst_temp_dir)
        # Extract XML Sheet Files
        with zipfile.ZipFile(dst_temp_dir,'r') as zip_ref:
            ziptmp = os.path.join(rtemp, 'zip')
            createFolder(ziptmp)
            zip_ref.extractall(ziptmp)
            modxmlpath = os.path.join(ziptmp, 'xl', 'worksheets')
            modxmltree = os.listdir(modxmlpath)
            # Modify the XML Files
            for mxml in modxmltree:
                if(mxml.endswith('.xml')):
                    findPasswordLine(os.path.join(modxmlpath, mxml))

            create_zip_from_directory(ziptmp, os.path.join(rtemp, 'temp.zip'), dst_exp_dir)
            # Cleanup the existing files to avoid corruption on multiple Excel Inputs
            cleanupTemp(ziptmp)
    # Delete the Temp folder. Noone needs it afterwards
    if dst_exp_dir is None:
        printRed('No files found on the server')
    cleanupTemp(reppytemp)
    return dst_exp_dir

def removePassword(pyimport, pyexport):
    exception = ''
    try:
        reppydirs(pyimport, pyexport)
        return main(reppyimport, reppytemp, reppyexport), exception
    except Exception as ex:
        message = 'Exception raised: {}'.format(ex)
        traceback.print_exc()
        cleanupTemp(reppytemp)
        printRed(message)
        return None, message

if __name__ == '__main__':
    removePassword('import', 'export')
