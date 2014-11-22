# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        log
# Purpose:     Implements shared logging functionality.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------
import logging

LOG_FILENAME = 'RUIANDownload.log'


def clearLogFile():
    with open(LOG_FILENAME, 'w'):
        pass

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

