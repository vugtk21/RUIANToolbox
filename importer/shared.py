# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        shared
# Purpose:
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

firstCall = True
RUIANToolBoxPath = ""


def setupPaths(depth = 1):
    # ####################################
    # Setup path to RUIANToolbox
    # ####################################
    global RUIANToolBoxPath
    global firstCall

    if firstCall:
        import os.path, sys

        pathParts = os.path.dirname(__file__).split(os.sep)
        basePath = os.sep.join(pathParts[:len(pathParts) - depth])

        RUIANToolBoxPath = basePath

        if not basePath in sys.path:
            sys.path.append(basePath)
        firstCall = False