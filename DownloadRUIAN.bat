@echo off
echo Tento skript stahuje data z VDP
echo -------------------------------
echo Pro informaci o prubehu stahovani, sledujte obsah souboru DownloadRUIAN.log a DownloadRUIANErr.log, pripadne ostatni logovaci soubory v adresari se stazenymi daty.
echo Download muze trvat pri pomalem pripojeni k internetu nekolik desitek minut.
echo -------------------------------
echo !!!Nezavirejte toto okno do ukonceni davky!!!
cd RUIANDownloader
RUIANDownload.py >>..\DownloadRUIAN.log 2>>..\DownloadRUIANErr.log
cd ..