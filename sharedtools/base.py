# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sharetools
# Purpose:     Library shared procedures.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import os, sys, codecs


RUNS_ON_WINDOWS = sys.platform.lower().startswith('win')
RUNS_ON_LINUX = not RUNS_ON_WINDOWS
COMMAND_FILE_EXTENSION = [".bat", ".sh"][RUNS_ON_LINUX]


def extractFileName(fileName):
    lastDel = fileName.rfind(os.sep)
    return fileName[lastDel + 1:]


def getFileExtension(fileName):
    """ Returns fileName extension part dot including (.txt,.png etc.)"""
    return fileName[fileName.rfind("."):]


def pathWithLastSlash(path):
    assert isinstance(path, basestring)

    path = normalizePathSep(path)
    if path != "" and path[len(path) - 1:] != os.sep:
        path = path + os.sep

    return path


def createDirForFile(fileName):
    safeMkDir(os.path.dirname(fileName))


def safeMkDir(path):
    assert isinstance(path, basestring)

    if path == "" or os.path.exists(path): return

    pathParts = path.split(os.sep)
    actPathList = []
    for pathItem in pathParts:
        actPathList.append(pathItem)
        actPathStr = os.sep.join(actPathList)
        if actPathStr and not os.path.exists(actPathStr):
            os.mkdir(actPathStr)

def extractFileName(path):
    head, tail = os.path.split(path)

    return tail


def getPythonModules():
    return sys.modules.keys()


def setupUTF():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')


def normalizePathSep(path):
    assert isinstance(path, basestring)

    path = path.replace("/", os.sep)
    path = path.replace("\\", os.sep)

    return path


def getFileContent(fileName, charSet = "utf-8"):
    assert isinstance(fileName, basestring)
    assert isinstance(charSet, basestring)

    if os.path.exists(fileName):
        inFile = codecs.open(fileName, "r", charSet)
        result = inFile.read()
        inFile.close()
    else:
        result = ""

    return result


