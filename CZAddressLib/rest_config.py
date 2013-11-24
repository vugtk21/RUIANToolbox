#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

# Local configuration file, don't deploy to central repository GIT

# CONFIGURATION
if True:
    SERVER_HTTP = 'localhost'
    PORT_NUMBER = 8086
    SERVICES_WEB_PATH = "E:\\02_OpenIssues\\07_Euradin\\Euradin\\HTML\\"
    SERVER_PATH_DEPTH = 1 # Služba rest je první za HTTP serverem
    HTMLDATA_URL = 'http://localhost/RuianServices/'
else:
    SERVER_HTTP = '192.168.1.130'
    PORT_NUMBER = 8080
    SERVICES_WEB_PATH = "services_WEB/"
    SERVER_PATH_DEPTH = 0
# END OF CONFIGURATION