__author__ = 'raugustyn'

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

