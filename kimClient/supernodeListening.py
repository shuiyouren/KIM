from socket import *
from supernodeListen import *
import threading
import xml.parsers.expat
import string
import time

class supernodeListening (threading.Thread):
    def __init__(self, port, host, server_name, sessionid):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.server_name = server_name
        self.sessionid = sessionid
        self.running = True
        self.connect_a = set ()
        #self.onMessage = None
    def run (self):
        s = socket(AF_INET, SOCK_STREAM)
        print "Kim Supernode"
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
            connect = supernodeListen ( connection, self.server_name )
            connect.start()
            connect.setOnMessage ( self.onMessage )
            self.connect_a.add ( connect )
        s.close()
    
    def onMessage(self, from_, to, body, type_):
        for conn in self.connect_a:
            print "Search '%s' '%s'" % (conn.username, to)
            if conn.username == to:
                print "Match!"
                conn.sendMessage ( from_, to, body, type_ )
    
    def stop (self):
        print "serverListenning STOP (running False)"
        self.running = False
