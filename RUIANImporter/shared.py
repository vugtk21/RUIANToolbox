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

def setupPaths():
    # ####################################
    # Setup path to RUIANToolbox
    # ####################################
    if firstCall:
        import os.path, sys

        pathParts = os.path.dirname(__file__).split(os.sep)
        basePath = os.sep.join(pathParts[:len(pathParts) - 1])
        #basePath = os.path.join(os.path.dirname(__file__), "../..")
        if not basePath in sys.path:
            sys.path.append(basePath)
            print sys.path
            print "Base path:", basePath
        global firstCall
        firstCall = False
