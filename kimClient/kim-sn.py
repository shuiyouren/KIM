#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
import threading
import xml.parsers.expat
import string
import time

PUERTO_SERVER = 5333
SERVER_HOST = 'localhost'
PUERTO_SUPERNODE = 5334

server = 'kimly.org'

connect_a = set ()

KILL = False

class Supernode(threading.Thread):
    def __init__(self, port, host):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.jobs = list ()
        self.running = True
        self.snsessionid = None
    
    def run (self):
        print "Kim Supernode"
        print "Connecting to server %s at port %s" % ( SERVER_HOST, PUERTO_SERVER)
        self.snsessionid = self.serverAuth ().execute ()
        print "Connected SNSID: %s" % self.snsessionid
        listening = self.Listening (self)
        listening.start()
        while not KILL:
            #if self.running == False:
                #listening.join()
            #print 'While'
            time.sleep(1)
        print 'End'
        
        
    
    class Listening (threading.Thread):
        def __init__(self, father):
            threading.Thread.__init__(self)
            #self.type = connection
            #self.jid = address
            #self.data = list ()
            self.running = True
            self.father = father
        def run (self):
            s = socket(AF_INET, SOCK_STREAM)
            print "Kim Supernode"
            print "Connecting to port %s" % PUERTO_SUPERNODE
            trya = True
            while trya:
                trya = False
                try:
                    s.bind(('', PUERTO_SUPERNODE))
                except:
                    trya = True
            s.listen(5)
            print "Listening"
            while self.running:
                connection, address = s.accept()
                connect = self.Listen (self, connection, address )
                connect.start()
                connect_a.add ( connect )
            self.father.running = False

        class Listen(threading.Thread):
            def __init__(self, father, connection, address ):
                threading.Thread.__init__(self)
                self.connection = connection
                self.address = address
                self.name = ''
                self.result = ''
                self.done = False
                self.lastcont = None
                self.streamid = None
                self.sessionid = None
                self.do = None
                self.connected = True
                self.father = father
                self.characteris = None
                self.username = None
                self.password = None
            def run (self):
                while self.connected:
                    data = self.connection.recv(1024) # receive up to 1K bytes
                    data = string.rstrip ( data )
                    if not data: break
                    
                    self.result = None
                    self.queryId = None
                    self.type_ = None
                    
                    #Parse:
                    #"<?xml version='1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' to='kimly.org' xmlns='kim:client'>"
                    def start_element(name, attrs):
                        print 'Start element:', name, attrs 
                        if ( name == 'stream:stream'):
                            self.streamid = '123'
                            if attrs['xmlns:stream'] != 'http://etherx.kimly.org/streams':
                                return
                            if attrs['xmlns'] == 'kim:node':
                                self.conntype = 'node'
                            elif attrs['xmlns'] == 'kim:supernode':
                                self.conntype = 'supernode'
                            else:
                                return
                            if attrs['to'] != server:
                                return
                            self.result = "<?xml version = '1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' id='%s' xmlns='kim:%s' from='%s'>" % (self.streamid, self.conntype, server)
                            self.done = True
                            #self.send_result ()
                        if ( self.streamid == None ):
                            return
                        if ( name == 'iq'):
                            self.queryId = attrs['id']
                            self.type_ =  attrs['type']
                        if ( name == 'query'):
                            if (attrs['xmlns'] == 'kim:iq:auth' ):
                                if (self.type_ == 'get'):
                                    self.result = "<iq type='result' id='%s'><query xmlns='kim:iq:auth'><username>eibriel</username><password/></query></iq>" % self.queryId
                                if (self.type_ == 'set'):
                                    self.do = 'auth'
                        if ( name == 'username'):
                            self.characteris = 'username'
                        if ( name == 'password'):
                            self.characteris = 'password'
                        if ( name == 'sessionid'):
                            self.characteris = 'sessionid'
                    
                    def end_element(name):
                        print 'End element:', name
                    def char_data(data):
                        if self.characteris == 'username':
                            self.username = data
                        elif self.characteris == 'password':
                            self.password = data
                        elif self.characteris == 'sessionid':
                            self.sessionid = data
                        print 'Character data:', repr(data)
                    
                    
                    
                    #data = "%s</stream:stream>" % data
                    #p.Parse(data,1)
                    
                    try:
                        p = xml.parsers.expat.ParserCreate()
                        p.StartElementHandler = start_element
                        p.EndElementHandler = end_element
                        p.CharacterDataHandler = char_data
                        p.Parse(data,1)
                    except:
                        data = "%s</stream:stream>" % data
                    try:
                        p = xml.parsers.expat.ParserCreate()
                        p.StartElementHandler = start_element
                        p.EndElementHandler = end_element
                        p.CharacterDataHandler = char_data
                        p.Parse(data,1)
                    except:
                        print "ERRORRRRRR"
                        if self.sessionid == None:
                            self.connected = False
                            self.father.running = False
                            KILL = True
                            #print 'Data: %s' % data

                    if self.do == 'auth':
                        if (self.username == 'eibriel'):
                            #self.sessionid = time.time()
                            self.result = "<iq type='result' id='%s' />" % self.sessionid #self.queryId
                            self.done = True
                    if self.done == True:
                        self.send_result ()

                self.connection.close()
            
            def send (self, data):
                self.connection.send( data )
                
            def send_result (self):
                if self.result == None: return
                self.connection.send( self.result )

    class Job(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.type = connection
            self.jid = address
            self.data = list ()
        def run (self):
            if self.type == 'auth-n':
                print 'auth-n'
            if self.type == '':
                print 'auth-sn'
            if self.type == 'get-supernodes':
                print 'get-supernodes'



      
    class serverAuth ():
        def __init__(self):
            self.ret = True
            self.tempid = None
        
        def start_element(self, name, attrs):
            print 'Start element:', name, attrs
            if name == 'stream:stream':
                if attrs['xmlns:stream'] != 'http://etherx.kimly.org/streams':
                    ret = False
                if attrs['xmlns'] != 'kim:supernode':
                    ret = False
                if attrs['from'] != server:
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
            serverconn = self.serverConnection (SERVER_HOST, PUERTO_SERVER)
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
            def __init__(self, serverIP, serverPort ):
                self.socket = None
                self.serverIP = serverIP
                self.serverPort = serverPort
                self.lastcont = None
                print "Connecting"
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.connect((self.serverIP, self.serverPort))
                print "Connected to Server"
            def send (self, data):
                while self.socket == None:
                    #wait
                    h=1
                self.socket.send ( data )
            def recv ( self, cache ):
                return self.socket.recv( cache)
            def close (self):
                self.socket.close()

kisupernode = Supernode( PUERTO_SUPERNODE, '' )
kisupernode.start()
