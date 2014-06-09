# -*- coding: utf-8 -*-

# Local configuration file, don't deploy to central repository GIT

# CONFIGURATION
if False:
    SERVER_HTTP = 'www.vugtk.cz'
    PORT_NUMBER = 80
    SERVICES_WEB_PATH = "euradin/services/rest.py/"
    SERVER_PATH_DEPTH = 0
    HTMLDATA_URL = '/euradin/_euradin_services/'
else:
    SERVER_HTTP = 'localhost'
    PORT_NUMBER = 8080
    SERVICES_WEB_PATH = "services/"
    SERVER_PATH_DEPTH = 0
    HTMLDATA_URL = 'http://localhost/HTML/'
# END OF CONFIGURATION
