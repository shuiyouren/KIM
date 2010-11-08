from socket import *
from serverListening import *
import xml.parsers.expat
import string
import time

class serverThread:
    def __init__(self, port, host, server_name):
        self.port = port
        self.host = host
        self.server_name = server_name
        self.jobs = list ()
        self.running = True
        print 'Create serverThread'
        self.listening = serverListening (self.port, self.server_name)
        self.listening.start()
        print 'End serverThread'
        
    def stop (self):
        print "serverListening Stop"
        self.listening.stop()
