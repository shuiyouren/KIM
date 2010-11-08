from socket import *
from serverListen import *
import threading
import xml.parsers.expat
import string
import time

class serverListening(threading.Thread):
    def __init__(self, port, server_name):
        threading.Thread.__init__(self)
        #self.type = connection
        self.port = port
        self.server_name = server_name
        #self.data = list ()
        self.running = True
        self.connect_a = set ()
        
    def run (self):
        s = socket(AF_INET, SOCK_STREAM)
        print "Kim Server"
        print "Connecting to port %s" % self.port
        trya = True
        while trya:
            trya = False
            try:
                s.bind(('', self.port))
            except:
                trya = True
        s.listen(5)
        s.settimeout(0.5)
        print "Listening"

        while self.running:
            try:
                connection, address = s.accept()
            except:
                continue
            connect = Listen (connection, self.server_name )
            connect.start()
            self.connect_a.add ( connect)
            
        for conn in self.connect_a:
            self.connect_a.close()
            
    def stop (self):
        print "serverListenning STOP (running False)"
        self.running = False
            
