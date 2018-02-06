#!/bin/bash
echo Tento skript importuje data stazena z VDP do databaze.
echo ------------------------------------------------------
echo !!!Nezavirejte toto okno do ukonceni skriptu!!!

cd importer
python importruian.py
cd ..\
