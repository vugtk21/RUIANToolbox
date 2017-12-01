@echo off
echo Tento skript importuje data stazena z VDP do databaze.
echo ------------------------------------------------------
echo Pro informaci o prubehu importu, sledujte obsah souboru ImportRUIAN.log a ImportRUIANErr.log, pripadne ostatni logovaci soubory v adresari se stazenymi daty.
echo Import muze dle nastaveni a rychlosti pocitace trvat i nekolik hodin.
echo ------------------------------------------------------
echo !!!Nezavirejte toto okno do ukonceni skriptu!!!
cd importer
importruian.py %*  >> ..\ImportRUIAN.log 2>>&1 3>>..\ImportRUIANErr.log
cd ..\