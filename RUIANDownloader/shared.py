#-------------------------------------------------------------------------------
# Name:        shared
# Purpose:     Module shared procedures.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

firstCall = True
RUIANToolBoxPath = ""

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