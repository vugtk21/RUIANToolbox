# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

from urlparse import urlparse

class VDPParam:
    def __init__(self, name, title, values):
        self.name = name
        self.title = title
        self.values = values

class VDPParamValue:
    def __init__(self, value, queryString):
        self.value = value
        self.queryString = queryString

VDPParams = [
    VDPParam("vf.pu", "Platnost údajů",
             [ VDPParamValue(True, "vf.pu=S&_vf.pu=on&_vf.pu=on&"),
               VDPParamValue(False, "vf.pu=S&_vf.pu=on&_vf.pu=on&")
             ])
]

class Binder:
    def __init__(self, templateHRef):
        self.templateHRef = templateHRef
        parsedURL = urlparse(templateHRef)
        self.query = parsedURL.query.split("&")
        #self.fullData = self.query.get("", True)

        print parsedURL
        print self.query

b = Binder("http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat")

# TF vf.pu=S&_vf.pu=on&_vf.pu=on&           vf.cr=Z&vf.pd=02.03.2014&vf.ds=Z&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&search=Vyhledat
# TT vf.pu=S&_vf.pu=on&vf.pu=H&_vf.pu=on&   vf.cr=Z&vf.pd=02.03.2014&vf.ds=Z&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&search=Vyhledat
# FT _vf.pu=on&vf.pu=H&_vf.pu=on&           vf.cr=Z&vf.pd=02.03.2014&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&search=Vyhledat
# FF _vf.pu=on&_vf.pu=on&                   vf.cr=Z&vf.pd=02.03.2014&vf.ds=Z&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&search=Vyhledat