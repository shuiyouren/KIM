from socket import *
import threading
import xml.parsers.expat
import string
import time

class serverAuth:
    def __init__(self, server_host, server_port, server_name, username, password):
        
        self.server_port = server_port
        self.server_name = server_name
        self.server_host = server_host
        self.username = username
        self.password = password
        
        self.ret = True
        self.tempid = None
    
    def start_element(self, name, attrs):
        print 'Start element:', name, attrs
        if name == 'stream:stream':
            if attrs['xmlns:stream'] != 'http://etherx.%s/streams' % self.server_name:
                ret = False
            if attrs['xmlns'] != 'kim:supernode':
                ret = False
            if attrs['from'] != self.server_name:
                ret = False
        elif name == 'iq':
            if attrs['type'] == 'result':
                self.tempid = str(attrs['id'])
                print "tempid %s" % self.tempid
    def end_element(self, name):
        print 'End element:', name
    def char_data(self, data):
        print 'Character data:', repr(data)

    def execAuth(self, data):    
        error = False
        ret = True
        '''
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse(data,1)'''
        try:
            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = self.start_element
            p.EndElementHandler = self.end_element
            p.CharacterDataHandler = self.char_data
            p.Parse(data,1)
        except:
            data = "%s</stream:stream>" % data
            error = True
        if error:
            try:
                p = xml.parsers.expat.ParserCreate()
                p.StartElementHandler = self.start_element
                p.EndElementHandler = self.end_element
                p.CharacterDataHandler = self.char_data
                p.Parse(data,1)
            except:
                print "ERRORRRRRR"
                ret = False
                
        if self.tempid != None:
            print "tempid %s" % self.tempid
            return "%s" % self.tempid
        else:
            return ret
            
    def execute (self):
        serverconn = self.serverConnection (self.server_host, self.server_port)
        tosend = "<?xml version='1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' to='kimly.org' xmlns='kim:supernode'>"
        serverconn.send(tosend)
        print "%s\n\n" % tosend
        data = serverconn.recv(1024)
        print "%s\n\n" % data
        if self.execAuth ( data ) != True:
            serverconn.close()
            return False
        #Auth
        tosend = "<iq type='set' id='222'><query xmlns='kim:iq:auth'><username>eibriel</username><password>eibriel</password></query></iq>"
        serverconn.send(tosend)
        print "%s\n\n" % tosend
        data = serverconn.recv(1024)
        print "%s\n\n" % data
        res = self.execAuth ( data )
        print "res %s" % res
        serverconn.close()
        return res
        
    class serverConnection:
        def __init__(self, host, port ):
            self.socket = None
            self.host = host
            self.port = port
            self.lastcont = None
            print "Connecting"
            self.socket = socket(AF_INET, SOCK_STREAM)
            try:
                self.socket.connect((self.host, self.port))
            except:
                return
            print "Connected to Server"
            
        def send (self, data):
            while self.socket == None:
                #wait
                h=1
            try:
                self.socket.send ( data )
            except:
                return False
            return True
            
        def recv ( self, cache ):
            try:
                ret = self.socket.recv( cache)
            except:
                return False
            return ret
            
        def close (self):
            try:
                self.socket.close()
            except:
                return False
            return True
