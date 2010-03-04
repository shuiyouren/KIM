import threading, time, sys, xml.dom.minidom
from socket import *
from base import *
from cStringIO import StringIO


class refresh(threading.Thread):
    def __init__(self, myself, contacts, on_refresh ):
        threading.Thread.__init__(self)
        self.contacts = contacts
        self.on_refresh = on_refresh
        self.myself = myself
        self.debug = 0
        self.socket = None
        self.frequency = 0.1

        self.Sfrom = 0
        self.Sto = 255
        
    def run (self):
        while 1:
            #if self.debug>0: print " [refresh] REFRESH"
            time.sleep( self.frequency )
            self.ref ()

    def ref (self):
        contactPort = 1864
        for contact in self.contacts:
            time.sleep( self.frequency )
            status_set = 0
            contactOb = self.contacts [contact]
            if self.debug>2: print " [refresh] Open Socket"

            if self.debug>1: print "[refresh] Verifing %s status. To %s From: %s" % ( contact, contactOb['ip'], self.myself.ip )

            if contactOb['localip'] != '':
                if self.debug>1: print " [refresh]Local connection %s" % contactOb['localip']
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.settimeout(0.1)
                if self.connect (contactOb['localip'], contactPort, contact):
                    if self.debug>2: print "  [refresh] Conected!"
                    status_set = 1
                    if self.debug>1: print "OKKKKKKKKKKKKKK"
                else:
                    if self.socket!=None: self.socket.close
                    self.socket = None

            elif contactOb['ip'] == self.myself.ip:
                if self.debug>1: print "  [refresh]Local Net searching"
                if contactOb['localip'] == '':
                    for i in range( self.Sfrom, self.Sto):
                        self.socket = socket(AF_INET, SOCK_STREAM)
                        self.socket.settimeout(0.1)
                        if self.debug>2: print ( "SOCK: %s" % self.socket.getsockname() )
                        connectTo="192.168.1.%s" % (i)
                        if self.debug>2: print "   [refresh] Trying %s: %s" % ( connectTo, contactPort )
                        
                        if self.connect ( connectTo, contactPort, contact):
                            status_set = 1
                            self.contacts [contact]['localip'] = connectTo
                            break
                        else:
                            if self.socket!=None: self.socket.close
                            self.socket = None

            else:
                self.socket = socket(AF_INET, SOCK_STREAM)
                self.socket.settimeout(0.1)
                if self.debug>1: print " [refresh]Internet connection %s" % contactOb['ip']
                if self.connect (contactOb['ip'], contactPort, contact):
                    if self.debug>2: print "  [refresh] Conected!"              
                    status_set = 1
                else:
                    if self.socket!=None: self.socket.close
                    self.socket = None

            if self.debug>1: print "SET: "+str(status_set)

            if status_set == 0:
                self.contacts [contact]['connected'] = 0
                continue
            else:
                self.contacts [contact]['connected'] = 1

            #if status_set == 0:
            #    if self.debug>0: print "SETTING OFFLINE"
            #    self.contacts [contact]['status'] = status.OFFLINE

            contactOb = self.contacts [contact]

            self.on_refresh ( contactOb )

            if self.debug>2: print " [refresh] Close Socket"
            if self.socket!=None: self.socket.close
            self.socket = None

    def connect (self, host, port, contact):
        try:
            self.socket.connect((host, port))
        except:
            if self.debug>2:  print "  [refresh] Connection error %s" % sys.exc_info()[0]
            return 0
        else:
            if self.debug>2: print "  [refresh] Conected!"              
            if self.getstatus ( self.socket, contact ):
                return 1

    def getstatus (self, socket, contact):
        toSend = StringIO()
        toSend.write ("<connection>")
        toSend.write (" <type>status_request</type>")
        toSend.write (" <recipient>%s</recipient>" % contact)
        toSend.write ("</connection>")
        toSend.seek(0)

        try:
            socket.send( toSend.read() )
        except:
            if self.debug>2: print "  [refresh] Error sending request"
            return 0
        
        if self.debug>1: print "  [refresh] Sending Request: %s" % toSend.read()
        try:
            data = socket.recv(1024)
        except:
            if self.debug>0: print "  [refresh] Error geting responce"
            return 0

        if self.debug>1: print "  [refresh] Status Data: "+data

        cstatus = 'offline'

        try:
            doc = xml.dom.minidom.parseString( data )
        except:
            if self.debug>0: print "  [refresh] Error parsing XML: %s" % sys.exc_info()[0]
            return 0

        try:
            if doc.getElementsByTagName('status')[0].firstChild.nodeValue == 'error':
                if self.debug>1: print "  [refresh] Error response "
                doc.unlink()
                return 0
        except:
            pass

        try:
            cstatus = doc.getElementsByTagName('pstatus')[0].firstChild.nodeValue
        except:
            if self.debug>0: print "  [refresh] Error extracting data info: %s" % sys.exc_info()[0]
            doc.unlink()
            return 0

        if cstatus == 'busy':
            if self.debug>1: print "  [refresh]%s is Busy." % contact
            stat = status.BUSY
        elif cstatus == 'away':
            if self.debug>1: print "  [refresh]%s is Away." % contact
            stat = status.AWAY
        elif cstatus == 'idle':
            if self.debug>1: print contact+" is Idle."
            stat = status.IDLE
        elif cstatus == 'online':
            if self.debug>1: print "  [refresh]%s is Online." % contact
            stat = status.ONLINE
        elif cstatus == 'offline':
            if self.debug>1: print "  [refresh]%s is Offline." % contact
            stat = status.OFFLINE
        else:
            if self.debug>1: print "  [refresh]%s is Else." % contact
            stat = status.IDLE


        if self.debug>2: print "SSSSSSSSSSSSSSSSSSSS: %s" % stat
        self.contacts[ contact ]['status'] = stat

        doc.unlink()

        return 1
