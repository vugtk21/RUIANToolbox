#!/bin/bash
echo Tento skript stahuje data z VDP
echo -------------------------------
echo Pro informaci o prubehu stahovani, sledujte obsah souboru DownloadRUIAN.log
echo a DownloadRUIANErr.log, pripadne ostatni logovaci soubory v adresari se
echo stazenymi daty.
echo Download muze trvat pri pomalem pripojeni k internetu nekolik desitek minut.
echo Pokud je konfigurace nastavena tak, aby ihned po stazeni byla data importovana
echo do databaze, muze byt cely ukoncen az za nekolik hodin.
echo -------------------------------
cd downloader
# Edit note: Presmerovani vystupu do logu odebrano kvuli kontajnerizaci
python downloadruian.py
cd ..