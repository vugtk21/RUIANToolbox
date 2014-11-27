@echo off
cd RUIANImporter
importRUIAN.py %*  >> ..\importRUIAN.log 2>>..\importRUIANErr.log
cd ..\