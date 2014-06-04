# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import compileaddress
import fulltextsearch
import geocode
import nearbyaddresses
import validate
import validateaddressid

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    tester = sharedtools.FormalTester("Všechny testy")

    compileaddress.test(tester)
    fulltextsearch.test(tester)
    geocode.test(tester)
    nearbyaddresses.test(tester)
    validate.test(tester)
    validateaddressid.test(tester)

    tester.saveToHTML("TestResults.html")