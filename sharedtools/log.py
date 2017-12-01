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


def clearLogFile(logFileName):
    " This procedure creates empty log file with file name LOG_FILENAME "
    f = open(logFileName, 'w')
    f.close()


def createLogger(logFileName):
    global logger

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s %(message)s', datefmt="%H:%M:%S")

    # Create and setup console log parameters
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s %(message)s', "%H:%M:%S"))
    logger.addHandler(ch)

    # Create and setup log file parameters
    createDirForFile(logFileName)
    fileHandler = logging.FileHandler(logFileName)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)


if __name__ == '__main__':
    logger.info("Logger test info")
    logger.debug("Logger test debug")
    logger.error("Logger test error")
    logger.critical("Logger test critical")