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

LOG_FILENAME = 'RUIANDownload.log'


def clearLogFile():
    " This procedure creates empty log file with file name LOG_FILENAME "
    f = open(LOG_FILENAME, 'w')
    f.close()

# create logger
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

# Create and setup console log parameters
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s %(message)s', "%H:%M:%S"))
logger.addHandler(ch)

# Create and setup log file parameters
fileHandler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

