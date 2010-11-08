import threading
from kimConn import *
from nodeFramer import *
import string

class nodeConnection (threading.Thread):
    def __init__(self, supernode_port, supernode_host, server_name, sessionid):
        threading.Thread.__init__(self)
        self.supernode_port = supernode_port
        self.supernode_host = supernode_host
        self.sessionid = sessionid
        self.jobs = list ()
        self.running = True
        self.snodeconn = None
        
    def run (self):
        print "Connecting to supernode %s at port %s" % ( self.supernode_host, self.supernode_port)
        self.snodeconn = kimConn (self.supernode_host, self.supernode_port )
        if self.snodeconn.error == '':
            tosend = "<?xml version='1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' to='kimly.org' xmlns='kim:node'>"
            print "%s\n\n" % tosend
            self.snodeconn.send ( tosend )
            data = self.snodeconn.recv(1024)
            print "%s\n\n" % data
            tosend = "<iq type='set' id='222'><query xmlns='kim:iq:auth'><username>eibriel</username><sessionid>%s</sessionid></query></iq>" % self.sessionid
            print "%s\n\n" % tosend
            self.snodeconn.send ( tosend )
            data = self.snodeconn.recv(1024)
            print "%s\n\n" % data
        else:
            print "Can not connect to Server"
            return False
        
        self.theFramer = nodeFramer ( self.snodeconn)
        self.theFramer.start()
        
        while 1:
            data = self.snodeconn.recv(1024)
            data = string.rstrip (data)
            if data=='message': print data
        
    def send (self, data):
        self.theFramer.addToSend( data )
        
    def close (self):
        print "supernodeListening Stop"
        self.snodeconn.close()
