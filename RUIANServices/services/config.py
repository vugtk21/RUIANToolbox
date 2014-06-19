__author__ = 'Augustyn'

# Setup path to RUIANToolbox
import os.path, sys
basePath = os.path.join(os.path.dirname(__file__), "../..")
if not basePath in sys.path: sys.path.append(basePath)

from SharedTools.Config import Config
import os

def convertServicesCfg(config):
    if config == None: return

    if config.portNumber == "":
        config.portNumber = 80
    else:
        config.portNumber = int(config.portNumber)
    pass

    if config.servicesWebPath[len(config.servicesWebPath)-1:] == "/":
        config.servicesWebPath = config.servicesWebPath[:len(config.servicesWebPath) - 1]

    if config.htmlDataURL != "" and config.htmlDataURL[:1] == "/":
        config.htmlDataURL = config.htmlDataURL[1:]



config = Config(os.path.join(os.path.dirname(__file__), "RUIANServices.cfg"),
            {
                "serverHTTP" : 'www.vugtk.cz',
                "portNumber" : 80,
                "servicesWebPath" : "euradin/services/rest.py/",
                "htmlDataDir" : "Downloads\\",
                "htmlDataURL" : '/euradin/_euradin_services/'
            },
           convertServicesCfg)

SERVER_HTTP = config.serverHTTP
if config.portNumber == 80:
    PORT_SPECIFICATION = ""
else:
    PORT_SPECIFICATION = ":" + str(config.portNumber)

PORT_NUMBER = config.portNumber
SERVICES_WEB_PATH = config.servicesWebPath
HTMLDATA_URL = config.htmlDataURL



