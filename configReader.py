#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Radecek
#
# Created:     04/05/2013
# Copyright:   (c) Radecek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import configRUIAN

def getTableFields(tableName):
    if (configRUIAN.tableDef.has_key(tableName)):
        config = configRUIAN.tableDef[tableName]
        if config.has_key("field"):
             return config["field"].keys()
        else:
            return None

def main():
    pass

if __name__ == '__main__':
    main()
