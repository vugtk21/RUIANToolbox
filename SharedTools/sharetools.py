__author__ = 'raugustyn'

def getPythonModules():
    import sys
    return sys.modules.keys()

def setupUTF():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

