#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, threading, xml.parsers.expat, time
from socket import *
from kimConn import *


#serverIP = "kimly.org"
serverIP = "localhost"
serverPort = 5333

#supernodeIP = "kimly.org"
supernodeIP = "localhost"
supernodePort = 5334

server = 'kimly.org'

Tosend = None

#Get session id on server


class Node(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.port = port
        #self.host = host
        self.sessionid = None
    def run (self):
        print "Kim Node"
        print "Connecting to server %s at port %s" % ( serverIP, serverPort)
        self.sessionid = self.serverAuth ().execute ()
        print "Connected SNSID: %s" % self.sessionid
        #
        print "Connecting to supernode %s at port %s" % ( supernodeIP, supernodePort)
        snodeconn = kimConn (supernodeIP, supernodePort )
        if snodeconn.error == '':
            tosend = "<?xml version='1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' to='kimly.org' xmlns='kim:node'>"
            print "%s\n\n" % tosend
            snodeconn.send ( tosend )
            data = snodeconn.recv(1024)
            print "%s\n\n" % data
            tosend = "<iq type='set' id='222'><query xmlns='kim:iq:auth'><username>eibriel</username><sessionid>%s</sessionid></query></iq>" % self.sessionid
            print "%s\n\n" % tosend
            snodeconn.send ( tosend )
            data = snodeconn.recv(1024)
            print "%s\n\n" % data
        else:
            print "Can not connect to Server"
            return False
        
        theFramer = self.framer (snodeconn)
        theFramer.start()
        Tosend = ''
        while Tosend!="exit":
            Tosend = raw_input("Message: ")
            self.send(Tosend)
        

    class framer (threading.Thread):
        def __init__(self, snodeconn):
            threading.Thread.__init__(self)
            self.snodeconn = snodeconn
        def run (self):
            while 1:
                time.sleep (1.5)
                if Tosend=='':
                    Tosend = "<iq type='ping'>"
                else:
                    print Tosend
                self.snodeconn.send (Tosend)
                Tosend = ''

    def send (self, Tosend_):
        Tosend = "%s %s" % (Tosend, Tosend_)

    class serverAuth:
        def __init__(self):
            self.ret = True
            self.tempid = None
        
        def start_element(self, name, attrs):
            print 'Start element:', name, attrs
            if name == 'stream:stream':
                if attrs['xmlns:stream'] != 'http://etherx.kimly.org/streams':
                    ret = False
                if attrs['xmlns'] != 'kim:node':
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
                '''
                p = xml.parsers.expat.ParserCreate()
                p.StartElementHandler = self.start_element
                p.EndElementHandler = self.end_element
                p.CharacterDataHandler = self.char_data
                p.Parse(data,1)
                '''
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
            serverconn = self.serverConnection (serverIP, serverPort)
            tosend_ = "<?xml version='1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' to='kimly.org' xmlns='kim:node'>"
            serverconn.send(tosend_)
            print "%s\n\n" % tosend_
            data = serverconn.recv(1024)
            print "%s\n\n" % data
            if self.execAuth ( data ) != True:
                serverconn.close()
                return False
            #Auth
            tosend_ = "<iq type='set' id='222'><query xmlns='kim:iq:auth'><username>eibriel</username><password>eibriel</password></query></iq>"
            serverconn.send(tosend_)
            print "%s\n\n" % tosend_
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
                
kinode = Node()
kinode.start()
kinode.join()
