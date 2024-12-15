import os
import sys

def createDirectory(path):
    """ Creates a directory if it doesn't exist yet. """
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
        return True
    
    return False

def checkFileExists(path):
    """ Checks if a needed file exists """
    if os.path.isfile(path):
        return True

    return False