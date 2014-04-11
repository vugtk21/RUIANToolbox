#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

__author__ = 'Liska'

from HTTPShared import *

def FindAddress(ID, builder):
    if ID == "12356":
        lines = [u"Lhenická 1120/1",u"České Budějovice 2",u"37005 České Budějovice"]
    else:
        lines = []
    return builder.listToResponseText(lines)