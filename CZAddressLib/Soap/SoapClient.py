import SOAPpy
server = SOAPpy.SOAPProxy("http://localhost:9080/")
for i in range(0, 100):
    print i, server.radecek()