__author__ = 'Augustyn'

from SharedTools.Config import Config

def convertServicesCfg(config):
    if config == None: return

    if config.portNumber == "":
        config.portNumber = 0
    else:
        config.portNumber = int(config.portNumber)
    pass

config = Config("RUIANDownload.cfg",
            {
                "serverHTTP" : 'www.vugtk.cz',
                "portNumber" : 80,
                "servicesWebPath" : "euradin/services/rest.py/",
                "htmlDataDir" : "Downloads\\",
                "htmlDataURL" : '/euradin/_euradin_services/'
            },
           convertServicesCfg)

SERVER_HTTP = config.serverHTTP
PORT_NUMBER = config.portNumber
SERVICES_WEB_PATH = config.servicesWebPath
HTMLDATA_URL = config.htmlDataURL



