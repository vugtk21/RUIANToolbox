#-------------------------------------------------------------------------------
# Name:        DB structure
# Purpose:
#
# Author:      Ota
#
# Created:     02.05.2013
# Copyright:   (c) Ota 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# -*- coding: utf-8 -*-

import configRUIAN

def main():
    pass

if __name__ == '__main__':
    main()

ruianPostGISTableStructure = configRUIAN.getRuianPostGISTableStructure()

for items in ruianPostGISTableStructure:
    print '-- ' + items
    print ruianPostGISTableStructure[items]