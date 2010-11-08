from socket import *
import threading
import xml.parsers.expat
import time

class Listen(threading.Thread):
    def __init__(self, connection, server_name ):
        threading.Thread.__init__(self)
        self.connection = connection
        self.server_name = server_name
        self.name = ''
        self.result = ''
        self.done = False
        self.lastcont = None
        self.streamid = None
        self.sessionid = None
        self.snsessionid = None
        self.do = None
        self.running = True
        #self.father = father
        self.characteris = None
        self.username = None
        self.password = None
        self.conntype = None
    def run (self):
        while self.running:
            data = self.connection.recv(1024) # receive up to 1K bytes
            data = string.rstrip ( data )
            if not data: break
            
            self.result = None
            self.queryId = None
            self.type_ = None
            
            #Parse:
            #"<?xml version='1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' to='kimly.org' xmlns='kim:client'>"
            def start_element(name, attrs):
                #print 'Start element:', name, attrs 
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
                    if attrs['to'] != self.server_name:
                        return
                    self.result = "<?xml version = '1.0'?><stream:stream xmlns:stream='http://etherx.kimly.org/streams' id='%s' xmlns='kim:%s' from='%s'>" % (self.streamid, self.conntype, self.server_name)
                    self.done = True
                    #self.send_result ()
                if ( self.streamid == None ):
                    return
                if ( name == 'iq'):
                    self.queryId = attrs['id']
                    self.type_ =  attrs['type']
                    if self.type == 'ping'
                        self.done = True
                        self.result = ""
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
            
            def end_element(name):
                ''''''
                #print 'End element:', name
            def char_data(data):
                if self.characteris == 'username':
                    self.username = data
                if self.characteris == 'password':
                    self.password = data
                #print 'Character data:', repr(data)
            
            
            #print "Data: %s" % data
            #data = "%s</stream:stream>" % data
            #p.Parse(data,1)
            
            '''
            p = xml.parsers.expat.ParserCreate()
            p.StartElementHandler = start_element
            p.EndElementHandler = end_element
            p.CharacterDataHandler = char_data
            p.Parse(data,1)'''
                
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
                    self.running = False
                    #self.father.running = False
                    #KILL = True
                    #print 'Data: %s' % data

            if self.do == 'auth':
                if self.conntype == 'node':
                    if (self.username == 'eibriel') and (self.password == 'eibriel'):
                        self.sessionid = time.time()
                        self.result = "<iq type='result' id='%s' />" % self.sessionid #self.queryId
                        self.done = True
                elif self.conntype == 'supernode':
                    if (self.username == 'eibriel') and (self.password == 'eibriel'):
                        self.snsessionid = time.time()
                        self.result = "<iq type='result' id='%s' />" % self.snsessionid #self.queryId
                        self.done = True
            if self.done == True:
                self.send_result ()

        self.connection.close()

    def sendMessage (self, from_, to, body, type_):
        print "SENDING"
        self.connection.send ( '<message to="%s" from="%s" type="%s">%s</message>' % (to, from_, type_, body) )

    def close (self):
        self.connection.close()
        
    def stop (self):
        self.connection.close()

    def send (self, data):
        self.connection.send( data )
        
    def send_result (self):
        if self.result == None: return
        self.connection.send( self.result )
