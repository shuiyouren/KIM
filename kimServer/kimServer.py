from serverThread import *

class kimServer:
    def __init__(self, port, name, host):
    
        self.port = port
        self.name = name
        self.host = host
    
        self.kiserver = serverThread( self.port, '', self.name )
        
    def stop (self):
        print "serverThread STOP"
        self.kiserver.stop()
