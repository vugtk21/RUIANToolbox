echo off
cd RUIANImporter
importRUIAN.py %*
..\OSGeo4W_vfr\OSGeo4W.bat download.bat
cd ..\