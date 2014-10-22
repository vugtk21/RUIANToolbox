#!C:/Python27/python.exe

from shutil import copyfileobj
import sys

if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

#sys.stdout.mode = "wb"

#print "Content-Type: text/plain;charset=utf-8"   # HTML is following
#print                                           # blank line, end of headers
print "Content-type: application/octet-stream"
print "Content-Disposition: attachment; filename=tacr_eng.png"
print

pngFile = open('C:/Users/raugustyn/Desktop/RUIAN/RUIANToolbox/RUIANServices/HTML/tacr_eng.png','rb')
sys.stdout.write(pngFile.read())
#copyfileobj(pngFile, sys.stdout)
pngFile.close()
sys.stdout.flush()

