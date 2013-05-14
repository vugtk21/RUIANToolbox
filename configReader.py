# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        configReader
# Purpose:     Pomocné funkce pro interpretaci knihovny configRUIAN.py
#
# Author:      Radek Augustýn
#
# Created:     04/05/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import configRUIAN

def getTableFields(tableName):
    """ Vrací definici sloupců v tabulce tableName.

        @param tableName {String} Název tabulky, jejiž definici sloupců hledáme

        @Return {Dict} Seznam sloupců tabulky tableName
                None   Jestliže tabulka tableName není nalezena.

    """
    if (configRUIAN.tableDef.has_key(tableName)):
        config = configRUIAN.tableDef[tableName]
        if config.has_key("fields"):
             return config["fields"].keys()
        else:
            return None