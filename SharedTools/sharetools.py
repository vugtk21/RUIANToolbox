# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sharetools
# Purpose:     Library shared procedures.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import os

def safeMkDir(path):
    if path == "" or os.path.exists(path): return

    pathParts = path.split(os.sep)
    actPathList = []
    for pathItem in pathParts:
        actPathList.append(pathItem)
        actPathStr = os.sep.join(actPathList)
        if not os.path.exists(actPathStr):
            os.mkdir(actPathStr)
    pass

def getPythonModules():
    import sys
    return sys.modules.keys()

def setupUTF():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

def normalizePathSep(path):
    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)
    return path

def getFileContent(fileName, charSet = "utf-8"):
    if os.path.exists(fileName):
        import codecs
        inFile = codecs.open(fileName, "r", charSet)
        result = inFile.read()
        inFile.close()
    else:
        result = ""

    return result


