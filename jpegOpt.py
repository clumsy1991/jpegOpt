#! /usr/bin/python -B

###############################################################
########                  jpegOpt.py                   ######## 
########             Made by Thomas Roberts            ######## 
########                  31/03/2016                   ########
###############################################################
from __future__ import division
from PIL import Image
import os
import sys
import logging
import fnmatch



# Search DIR for all files with a predfined suffix
# Input :- Path to the DIR
# Input :- The suffix
# Output :- All files in the path DIR with that suffix
def findRecursively(path, suffix):
    patten = "*." + suffix
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, patten):
            matches.append(os.path.join(root, filename))          

    return matches

# Optimise jpeg function
# Input :- Source DIR
# Input :- Destination DIR
# Output :- Boolean
# Description:- This function will optimise jpegs
def jpegOpt(source, destination, newQuality):
    # Return Value initialisations
    returnValue = True
    jpegs = []    
    logging.info("Scanning %s for jpegs", source)
    # Scan the sour DIR to find all APK's init
    #jpegs = [f for f in os.listdir(source) if f.endswith('jpg')]
    jpegs = findRecursively(source, "jp*g")
    
    if (len(jpegs) > 0):
        logging.info("Found %d jpegs to optimise", len(jpegs))
        for i in range(len(jpegs)):
            # Start optimising jepg's
            # Start optimising jepg's
            src = os.path.abspath(jpegs[i])
            dest =  os.path.abspath(jpegs[i].replace(source, destination))
            jpgDest = os.path.dirname(os.path.abspath(dest))
            if not os.path.isdir(jpgDest):
                os.makedirs(jpgDest)
            srcSize = os.path.getsize(src)
            image = Image.open(src)
            image.save(dest,optimize=True)
            destSize = os.path.getsize(dest)
            percentDiff = ((srcSize - destSize) / srcSize) * 100
            logging.info("Reduced image %s by %.2f %%", src, percentDiff)
    else:
        # We didn't find any jpeg's
        logging.error("Found no jpeg's in %s", source)
        returnValue = False

    return returnValue

# Check Arguments
# Input:- Source directory
# Input:- Destination directory
# Output:- Boolean, True is everything is ok
# This function will check the source and destination directory
def checkArgs(source, destination, quality):

    returnValue = True
    
    if not os.path.isdir(source):
        logging.error("Source directory %s doesn't exist", source)
        returnValue = False

    if not os.path.isdir(destination):
        logging.warning("Destination %s doesn't exist", destination)
        logging.info("Making destination directory as it doesn't exists")
        os.makedirs(destination)

    try:
        qual = int(quality)
        if (qual < 1):
            logging.error("The quality entered (%d) is less than 1, it needs to be between 1 and 100", qual)
            returnValue = False
        if (qual > 100):
            logging.error("The quality entered (%d) is more than 100, it needs to be between 1 and 100", qual)
            returnValue = False
    except ValueError:
        logging.error("The qualit entered (%s) is not a number", quality)    
        returnValue = False
        

    return returnValue

# Yes No Prompt
# Input:- Question
# Input:- default answer (default is yes unless changed)
# Output:- Boolean
# Description :- Prompt the user with a yes no question and return boolean.
def queryYesNo(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


# Clear shell script
# Input:- None
# Output:- None
# Description: This function will clear the shell 
def cls():
    os.system(['clear','cls'][os.name == 'nt'])

# Main
if __name__ == "__main__":
    # Initialise all logging configuration, only levels equal to info or above will be logged, the stream will be stdout and message will appear as the following:
    # DEBUG: This is DEBUG (only if configured)
    # INFO: This is information
    # Warning: This is a warning
    # Error: This is a error
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s: %(message)s')

    # Clean the shell
    cls()

    # Check arguments
    if len(sys.argv) > 1:
        if len(sys.argv) < 3 or len(sys.argv) > 5:
            logging.error("*** usage: %s <source directory> <destination directory> <new quality percent> \n",sys.argv[0])
        else:
            if (checkArgs(sys.argv[1], sys.argv[2], sys.argv[3])):
                jpegOpt(sys.argv[1], sys.argv[2], sys.argv[3])
            else:
                logging.error("Failed when checking arguments")
    else:
        # We have no arguments pass to use we will prompt the user
        src = raw_input("Please enter a source directory: ")
        dest = raw_input("Please enter a destination directory: ")
        newQuality = raw_input("Please enter new quality percent: ")

        if (checkArgs(src, dest, newQuality)):
            jpegOpt(src, dest, newQuality)
        else:
            logging.error("Failed when checking arguments")
    
    end = raw_input("\nDone! Press any key to exit....")