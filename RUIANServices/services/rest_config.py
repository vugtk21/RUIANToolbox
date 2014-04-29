# -*- coding: utf-8 -*-

# Local configuration file, don't deploy to central repository GIT

# CONFIGURATION
if False:
    SERVER_HTTP = '192.168.1.93'
    PORT_NUMBER = 8086
    SERVICES_WEB_PATH = "services/"
    SERVER_PATH_DEPTH = 0
    HTMLDATA_URL = '/euradin/_euradin_services/'
else:
    SERVER_HTTP = '192.168.1.130'
    PORT_NUMBER = 8080
    SERVICES_WEB_PATH = "services/"
    SERVER_PATH_DEPTH = 0
    HTMLDATA_URL = 'http://localhost/RuianServices/'
# END OF CONFIGURATION
