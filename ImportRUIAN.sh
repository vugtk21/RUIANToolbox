#!/bin/bash
@echo off
echo Tento skript importuje data stazena z VDP do databaze.
echo ------------------------------------------------------
echo Pro informaci o prubehu importu, sledujte obsah souboru ImportRUIAN.log a ImportRUIANErr.log, pripadne ostatni logovaci soubory v adresari se stazenymi daty.
echo Import muze dle nastaveni a rychlosti pocitace trvat i nekolik hodin.
echo ------------------------------------------------------
cd importer
# Edit note: Presmerovani vystupu do logu odebrano kvuli kontajnerizaci
python importruian.py
cd ..\