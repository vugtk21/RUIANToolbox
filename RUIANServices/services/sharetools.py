# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

def getKeyValue(dictWithValues, key, defaultValue = ""):
    if dictWithValues == None or not dictWithValues.has_key(key):
        return defaultValue
    else:
        return dictWithValues[key]

