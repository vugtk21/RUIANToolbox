#-------------------------------------------------------------------------------
# Name:        shared
# Purpose:
#
# Author:      Administrator
#
# Created:     08/10/2014
# Copyright:   (c) Administrator 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

firstCall = True
RUIANToolBoxPath = ""
isCGIApplication = True


def moduleExists(moduleName):
    import os
    return os.path.exists(RUIANToolBoxPath + os.sep + moduleName)

def setupPaths(depth = 1):
    # ####################################
    # Setup path to RUIANToolbox
    # ####################################
    if firstCall:
        import os.path, sys

        pathParts = os.path.dirname(__file__).split(os.sep)
        basePath = os.sep.join(pathParts[:len(pathParts) - depth])

        global RUIANToolBoxPath
        RUIANToolBoxPath = basePath

        if not basePath in sys.path:
            sys.path.append(basePath)
        global firstCall
        firstCall = False

def initApp(pathDepth = 1):
    setupPaths(pathDepth)
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
