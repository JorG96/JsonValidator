import os
from config import EXTENSION

def logSearch(dirName,ext=EXTENSION):
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file).replace("\\","/") for file in filenames if file.endswith(f"{ext}")]
    return listOfFiles
    