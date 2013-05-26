# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sharedTools
# Purpose:     y
#
# Author:      Radek Augustýn
#
# Created:     04/05/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os

def pathWithLastSlash(path):
    sepIdx = path.rfind(os.sep)
    if sepIdx == len(path) - 1:
        return path
    else:
        return path + os.sep

def getFileExtension(fileName):
    sepIdx = fileName.rfind(os.extsep)
    if sepIdx >= 0:
        return fileName[sepIdx + 1:]
    else:
        return ""
