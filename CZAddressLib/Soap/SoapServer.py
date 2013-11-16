import SOAPpy

def hello():
    return "Hello World"

def radecek():
    return "Ahoj radecku"

server = SOAPpy.SOAPServer(("localhost", 9080))
server.registerFunction(hello)
server.registerFunction(radecek)
server.serve_forever()
