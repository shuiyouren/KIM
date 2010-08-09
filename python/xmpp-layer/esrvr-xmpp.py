from socket import *
import threading
import xml.parsers.expat

IP_SERVIDOR = '127.0.0.1'
#IP_SERVIDOR = '75.101.138.128'
PUERTO_SERVIDOR = 5222
PUERTO = 5222

class Listen(threading.Thread):
    def __init__(self, port, host):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.debug = 10
    def run (self):
        s = socket(AF_INET, SOCK_STREAM)    # create a TCP socket
        s.bind((self.host, self.port))      # bind it to the server port
        s.listen(5)                         # allow 5 simultaneous
                                            # pending connections

        while 1:
            # wait for next client to connect
            connection, address = s.accept() # connection is a new socket
            while 1:
                data = connection.recv(1024) # receive up to 1K bytes
                if data:
                    send = ''
                    send = self.process_data (data)
                    if (send != None):
                        connection.send( send )
                    #connection.send("<?xml version = '1.0'?><stream:stream> xmlns:stream='http://etherx.jabber.org/streams' id='1234' xmlns='jabber:client' from='localhost'>")
                    print 'Data: %s' % data
                    print 'Send: %s' % send
                    print '-----'
                else:
                    break
            connection.close()              # close socket
   

    def process_data (self, data):
        if not data:
            return
        #print "  [eclient] receivingData: "+data
        #if (data[:5] == '<?xml'):
            #return
        
        self.result = None
        self.queryId = None
        self.type_ = None
        
         # 3 handler functions
        def start_element(name, attrs):
            print 'Start element:', name, attrs
            if ( name == 'stream:stream'):
                #print self.result
                self.result = "<?xml version = '1.0'?><stream:stream xmlns:stream='http://etherx.jabber.org/streams' id='2' xmlns='jabber:client' from='localhost'>"
                #print self.result
            #print "name %s" % name
            #nameStr = "%s" % name
            if ( name == 'iq'):
                self.queryId = attrs['id']
                self.type_ =  attrs['type']
            if ( name == 'query'):
                #print "ATTR %s" % attrs
                if (attrs['xmlns'] == 'jabber:iq:auth' ):
                    if (self.type_ == 'get'):
                        self.result = "<iq type='result' id='%s'><query xmlns='jabber:iq:auth'><username>eibriel</username><password/></query></iq>" % self.queryId
                    if (self.type_ == 'set'):
                        self.result = "<iq type='result' id='%s' />" % self.queryId
                if (attrs['xmlns'] == 'http://jabber.org/protocol/disco#info' ):#items
                    if (self.type_ == 'get'):
                        #data = s.recv(1024)
                        #self.result = "<presence from='oscar@jabber.es/trabajo' to='eibriel/Earendil'><status>Hola</status><show>chat</show></presence>"
                        self.result = "<iq type='result' id='%s' />" % self.queryId
                if (attrs['xmlns'] == 'jabber:iq:roster' ):
                    if (self.type_ == 'get'):
                        self.result = """<iq type='result' id='%s'><query xmlns='jabber:iq:roster'><item jid='sub1ID' name='nickname1'
                        subscription='both'>
                        <group>Personal</group>
                        <group>Trabajo</group>
                        </item>
                        </query>
                        </iq>""" % self.queryId
            if ( name == 'ping'):
                if (attrs['xmlns'] == 'urn:xmpp:ping' ):
                    self.result = "<iq type='result' id='%s' /><presence type='available' from='sub1ID' to='eibriel@localhost/Earendil'><status>LaaaLA</status><show>chat</show></presence>" % self.queryId
        def end_element(name):
            print 'End element:', name
        def char_data(data):
            print 'Character data:', repr(data)
        
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        try:
            p.Parse(data,1)
        except:
            print "ERRORRRRRR"
            if (self.result != None):
                return self.result
            else:
                return
        return self.result

        try:
            doc = xml.dom.minidom.parseString( data )
        except socket.error, msg:
            try:
                data = "%s</stream:stream>" % data
                doc = xml.dom.minidom.parseString( data )
            except socket.error, msg:
                if self.debug>0: print "[XMPPLayer] Invalid XML from client. %s" % msg
                print 'Fixed Data: %s' % data
                return
                #return "<?xml version='1.0'?><stream:stream xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams' id='1' from='localhost' version='1.0'><stream:error><xml-not-well-formed xmlns='urn:ietf:params:xml:ns:xmpp-streams'/></stream:error></stream:stream>"


        #<?xml version='1.0' ?>
        #Dato: <stream:stream to='localhost' xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams' version='1.0'>
        #Dato: <iq type='get' id='purple1a7aa150'><query xmlns='jabber:iq:auth'><username>eibriel</username></query></iq>

        get_stream = doc.getElementsByTagName('stream:stream')
        if (get_stream):
            return "<?xml version = '1.0'?><stream:stream xmlns:stream='http://etherx.jabber.org/streams' id='2' xmlns='jabber:client' from='localhost'>"
        
        type_ = doc.getElementsByTagName('iq')[0].firstChild.nodeValue

        if self.debug>1: print "   [eclient] Request Type: %s" % type_

        if type_=='message':
            sender = doc.getElementsByTagName('sender')[0].firstChild.nodeValue
            body = doc.getElementsByTagName('body')[0].firstChild.nodeValue
            self.on_message ( body, sender)
            doc.unlink()
            return "ok"
        elif type_=='status_request':
            if self.debug>1: print "    [eclient] To %s" % doc.getElementsByTagName('recipient')[0].firstChild.nodeValue  
            if doc.getElementsByTagName('recipient')[0].firstChild.nodeValue == self.user:
                if self.debug>1: print "    [eclient] Status Request" 
                if self.debug>1: print "request of %s to %s" % ( doc.getElementsByTagName('recipient')[0].firstChild.nodeValue, self.user )

                doc.unlink()

                if self.debug>1: print "    [eclient] Status: %s" % self.status_

                if self.status_ == status.BUSY:
                    mystatus = 'busy'
                elif self.status_ == status.AWAY:
                    mystatus = 'away'
                elif self.status_ == status.IDLE:
                    mystatus = 'idle'
                elif self.status_ == status.ONLINE:
                    mystatus = 'online'
                else:
                    return

                send = StringIO()
                send.write ('<connection>')
                send.write (' <type>status_answer</type>')
                send.write (' <pstatus>%s</pstatus>' % mystatus)
                send.write (' <user>%s</user>' % self.user)
                send.write (' <nick>%s</nick>' % self.nick)
                send.write (' <subnick>%s</subnick>' % self.subnick)
                send.write ('</connection>')
                send.seek(0)

                if self.debug>2: print "    [eclient] Answer: %s" % send.read()
                return send.read()
            else:
                return '<eserver><!-- Not Recipient --><status>error</status></eserver>'


listening = Listen( PUERTO, '' )
listening.start()
listening.join()
