import urllib, httplib, xml.dom.minidom, time, sys
from socket import *
from base import *
from listen import listen
from refresh import refresh
from http import http
from cStringIO import StringIO

class client:
    def __init__(self, user, password, host):
        self.debug = 0
        self.frequency = 0.1
        self.user = user
        self.password = password

        '''
        self.contacts = {}
        self.serverUrl = 'www.eibriel.com'
        self.serverPort = 80
        self.serverTimeout = 10
        self.nick = ''
        self.subnick = ''
        self.avatar = ''
        self.avatar_path = ''
        self.status_ = None
        self.stamp = None
        self.listener = None
        self.listener_files = None
        self.listener_voip = None
        self.listenSocket = None
        self.listenSocket_files = None
        self.listenSocket_voip = None
        self.refresher = None
        self.http = None
        self.cerror = None
        self.ip = ''
        self.localip = ''
        self.on_message = None
        self.on_contact_update = None
        '''
        

    def login ( self, initstatus, info_function ):
        elogin = login ( user, host, self.debug)


    def open_listenport ( self, port, maxconn, timeout ):
        if self.debug>0:  print "[eserver] Initializing listening"
        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        self.listenSocket_files = socket(AF_INET, SOCK_STREAM)
        #self.listenSocket_voip = socket(AF_INET, SOCK_STREAM)


        if self.debug>0: print " [eserver] Openning port 1864"
        self.listener = listen( 1864, self.listenSocket, self.receiveData )
        self.listener.debug = self.debug
        self.listener.start()

        if self.debug>0: print " [eserver] Openning port 1865"
        self.listener_files = listen( 1865, self.listenSocket_files, self.receiveData_files )
        self.listener_files.debug = self.debug
        self.listener_files.start()

    def start_refreshing (self):
        if self.debug>0: print "[eserver] Starting refresh"

        self.refresher = refresh ( self, self.contacts, self.contactUpdate )
        self.refresher.debug = self.debug
        self.refresher.frequency = self.frequency
        self.refresher.start()
        return

    def start_http (self):
        if self.debug>0: print "[eserver] Starting HTTP refresh"

        self.http = http ( self, self.contacts, self.contactUpdate, self.receiveData )
        self.http.debug = self.debug
        self.http.start()
        return

    def contactUpdate (self, contact ):
        #print "UUU:"+contact['user']
        self.contacts[ contact['user'] ] = contact
        self.on_contact_update ( contact )

    def addContact (self, contact):
        #try:
        serverconn = httplib.HTTPConnection( self.serverUrl , self.serverPort, timeout=self.serverTimeout)
        params = urllib.urlencode({'user': self.user, 'password': self.password, 'request': 'addcontact', 'contact': contact})
        retry = 1
        num = 0
        while retry:
            try:
                serverconn.request("GET", '/eserver/connection/?%s' % params )
            except:
                +num
                if num>2:
                    retry = 0
                else:
                    retry = 1
            else:
                retry = 0

        retry = 1
        num = 0
        while retry:
            try:
                response = serverconn.getresponse()
            except:
                +num
                if num>2:
                    retry = 0
                else:
                    retry = 1
            else:
                retry = 0

        serverconn.close()

        if response.reason=="OK":
            try:
                doc = xml.dom.minidom.parseString( response.read() )
            except:
                if self.debug>0:  print " [setnick] DATA ERR"
                self.cerror = error.DATA
                return 0
            else:
                error_ = doc.getElementsByTagName('error')[0].firstChild.nodeValue
                if error_ == 'ok':
                    if self.debug>0:  print " [setnick] OK"
                    self.cerror = None
                    doc.unlink()
                    return 1
                else:
                    self.cerror = error.AUTH
                    if self.debug>0:  print " [setnick] AUTH ERR"
                    doc.unlink()
                    return 0

    def getError (self):
        return self.cerror

    def getContactList (self):
        return self.contacts

    def getNick (self):
        return self.nick

    def getSubnick (self):
        return self.subnick

    def getAvatar (self):
        return self.avatar

    def getStamp (self):
        return int ( self.stamp )

    def setSomething (self, params):
        serverconn = httplib.HTTPConnection( self.serverUrl , self.serverPort, timeout=self.serverTimeout)
        retry = 1
        num = 0
        while retry:
            try:
                serverconn.request("GET", '/eserver/connection/?%s' % params )
            except:
                +num
                if num>2:
                    retry = 0
                else:
                    retry = 1
            else:
                retry = 0

        #except:
        #    self.cerror = error.CONN
        #    if self.debug>0:  print " [setnick] CONN ERR"
        #    return 0

        response = serverconn.getresponse()
        serverconn.close()

        if response.reason=="OK":
            try:
                doc = xml.dom.minidom.parseString( response.read() )
            except:
                if self.debug>0:  print "  [set] DATA ERR"
                self.cerror = error.DATA
                return 0
            else:
                error_ = doc.getElementsByTagName('error')[0].firstChild.nodeValue
                if error_ == 'ok':
                    if self.debug>0:  print "  [set] OK"
                    self.cerror = None
                    doc.unlink()
                    return 1
                else:
                    self.cerror = error.AUTH
                    if self.debug>0:  print "  [set] AUTH ERR"
                    doc.unlink()
                    return 0

    def setNick (self, nick):
        if self.debug>0:  print "SETNICK"
        params = urllib.urlencode({'user': self.user, 'password': self.password, 'request': 'setnick', 'nick': nick})
        return self.setSomething ( params )

            
    def setSubnick (self, subnick):
        if self.debug>0:  print "SETSUBNICK"
        params = urllib.urlencode({'user': self.user, 'password': self.password, 'request': 'setsubnick', 'subnick': subnick})
        return self.setSomething ( params )

    def setAvatar (self, avatar):
        if self.debug>0:  print "SETAVATAR"
        params = urllib.urlencode({'user': self.user, 'password': self.password, 'request': 'setavatar', 'avatar': avatar})
        return self.setSomething ( params )

    def sendMessage ( self, message, recipients ):

        #if self.debug>0: print "Recipients "+recipients


        if self.debug>0: print "Mensaje:"

        toSend = StringIO()
        toSend.write ("<connection>")
        toSend.write (" <type>message</type>")
        toSend.write (" <sender>%s</sender>" % self.user)
        toSend.write (" <body>%s</body>" % message)
        toSend.write ("</connection>")
        toSend.seek(0)


        if self.debug>0: print "Mensaje2: %s" % toSend.read()
        toSend.seek(0)


        #toSend ;
        #print [self.contacts[recipients]]
        if self.contacts[recipients]['connected']==0:
            if self.debug>0: print "   [eclient] HTTP Send message: %s to %s" % ( message, recipients )
            serverconn = httplib.HTTPConnection( self.serverUrl , self.serverPort, timeout=self.serverTimeout)
            params = urllib.urlencode({'user': self.user, 'password': self.password, 'request': 'send', 'xml': toSend.read(), 'recipient': recipients})
            retry = 1
            num = 0
            while retry:
                try:
                    serverconn.request("GET", '/eserver/connection/?%s' % params)
                except:
                    +num
                    if num>2:
                        retry = 0
                    else:
                        retry = 1
                else:
                    retry = 0
            #except:
            #    serverconn.close()
            #    return

            try:
                response = serverconn.getresponse()
            except:
                pass
            serverconn.close()
            return

        if self.debug>0: print "   [eclient] P2P Send message: %s" % message
        if self.contacts[recipients]['localip'] != '':
            recipientIp = self.contacts[recipients]['localip']
        else:
            recipientIp = self.contacts[recipients]['ip']

        ssend = socket(AF_INET, SOCK_STREAM)
        ssend.settimeout(1)

        recipientPort = 1864

        if self.debug>0: print "conecting... %s" % recipientIp

        try:
            ssend.connect(( recipientIp , recipientPort ))
        except:
            if self.debug>0: print "Connection failed. %s" % sys.exc_info()[0]
            return

        try:
            ssend.send( toSend.read() )
            toSend.seek(0)
        except:
            if self.debug>0: print "Fail Send. %s" % sys.exc_info()[0]

        if self.debug>0: print "Sending: %s" % toSend.read()
        #toSend.seek(0)
        try:
            data = ssend.recv(1024)
        except:
            if self.debug>0: print "Timeout."
        ssend.close()

    def receiveData ( self, data ):
        process.process_data( data )

    def receiveData_files ( self, data ):
        handle = file ( self.avatar_path, 'rb')
        avatar_raw = handle.read()
        handle.close()
        return avatar_raw

    def retrieveAvatar (self, user ):
        if self.debug>0: print "   [eclient] P2P Retreive Avatar: %s" % user

        if self.contacts [user]['connected'] != 1: return

        if self.contacts[user]['localip'] != '':
            recipientIp = self.contacts[user]['localip']
        else:
            recipientIp = self.contacts[user]['ip']

        ssend = socket(AF_INET, SOCK_STREAM)
        ssend.settimeout(3)

        recipientPort = 1865

        toSend ='avatar' ;

        if self.debug>0: print "conecting... %s" % recipientIp

        try:
            ssend.connect(( recipientIp , recipientPort ))
        except:
            if self.debug>0: print "Connection failed. %s" % sys.exc_info()[0]
            return

        try:
            ssend.send( toSend )
        except:
            if self.debug>0: print "Fail Send. %s" % sys.exc_info()[0]

        if self.debug>0: print "Sending: %s" % toSend
        try:
            #data = ssend.recv(1024)
            data = ssend.makefile()
        except:
            if self.debug>0: print "Timeout."

        ssend.close()

        return data

    def set_onMessage (self, function):
        self.on_message = function

    def set_onContactUpdate (self, function):
        self.on_contact_update = function

    def logout (self):
        if self.debug>0: print "LOGOUT"
        self.listener.stop
        self.listenSocket.close
        self.listenSocket_files.close
        self.refresher.stop
        self.http.stop

