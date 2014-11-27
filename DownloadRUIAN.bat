@echo off
cd RUIANDownloader
RUIANDownload.py >> ..\RUIANDownload.log 2>>..\RUIANDownloadErr.log
cd ..