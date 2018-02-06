# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        log
# Purpose:     This module creates standard logger for whole application.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------
import logging
from base import createDirForFile


logger = None

__tabLevel = 0
__indentLines = []
indent = ""


def __calcIndent():
    global indent

    indent = ""
    for i in range(__tabLevel):
        indent += "    "

    while len(__indentLines) < __tabLevel:
        __indentLines.append(0)


def incTabLevel():
    global __tabLevel

    __tabLevel += 1
    __calcIndent()


def decTabLevel():
    global __tabLevel

    __tabLevel = __tabLevel - 1
    if __tabLevel < 0:
        __tabLevel = 0

    __calcIndent()


def clearLogFile(logFileName):
    " This procedure creates empty log file with file name LOG_FILENAME "
    f = open(logFileName, 'w')
    f.close()


def __openSection(msg, level=logging.DEBUG):
    logger.debug(indent + msg)
    incTabLevel()


def __closeSection(msg="Done.", level=logging.DEBUG):
    decTabLevel()
    logger.debug(indent + msg)

def createLogger(logFileName):
    global logger

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s %(message)s', datefmt="%H:%M:%S")

    # Create and setup log file parameters
    createDirForFile(logFileName)
    fileHandler = logging.FileHandler(logFileName)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    logger.openSection = __openSection
    logger.closeSection = __closeSection


if __name__ == '__main__':
    logger.info("Logger test info")
    logger.debug("Logger test debug")
    logger.error("Logger test error")
    logger.critical("Logger test critical")