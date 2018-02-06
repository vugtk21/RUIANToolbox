#!/bin/bash
echo Tento skript stahuje data z VDP
echo -------------------------------
echo Download muze trvat pri pomalem pripojeni k internetu nekolik desitek minut.
echo Pokud je konfigurace nastavena tak, aby ihned po stazeni byla data importovana
echo do databaze, muze byt cely ukoncen az za nekolik hodin.
echo -------------------------------
cd downloader
python downloadruian.py
cd ..
