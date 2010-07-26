import threading, time, sys, xml.dom.minidom, httplib, urllib
from socket import *
from base import *

class http(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.serverUrl = "http://www.eibriel.com"
        self.debug = 0
        self.socket = None
        self.frequency = 7

        self.Sfrom = 0
        self.Sto = 255
        
    def run (self):
        while 1:
            #if self.debug>0: print " [refresh] REFRESH"
            time.sleep( self.frequency )
            self.loop ()

    def loop (self):
            if self.debug>0:  print "[http] Loop"
            #doc = None
            #serverconn = None
            #responce = None
            #status_ = None
            #params = None

            status_ = self.myself.status_
            serverconn = httplib.HTTPConnection( self.serverUrl , 80, timeout=10)
            params = urllib.urlencode({'user': self.myself.user, 'password': self.myself.password, 'request': 'refresh', 'info': 'yes', 'status': status_})
            try:
                serverconn.request("POST", '/eserver/index-example.php', params)
            except:
                if self.debug>0:  print "[http] CONN ERR"
                self.cerror = error.CONN
                serverconn.close()
                return

            try:
                response = serverconn.getresponse()
            except:
                if self.debug>0:  print "[http] CONN ERR"
                self.cerror = error.CONN
                serverconn.close()
                return

            serverconn.close()

            if response.reason=="OK":
                try:
                    doc = xml.dom.minidom.parseString( response.read() )
                except:
                    if self.debug>0:  print "[http] DATA ERR"
                    self.cerror = error.DATA
                else:
                    error_ = doc.getElementsByTagName('error')[0].firstChild.nodeValue

                    if error_ == 'ok':

                        self.nick = doc.getElementsByTagName('info')[0].getElementsByTagName('nick')[0].firstChild.nodeValue
                        self.subnick = doc.getElementsByTagName('info')[0].getElementsByTagName('subnick')[0].firstChild.nodeValue

                        contactsDom = doc.getElementsByTagName('contact')

                        self.myself.ip = doc.getElementsByTagName('clientip')[0].firstChild.nodeValue

                        self.myself.stamp = int (doc.getElementsByTagName('clientstamp')[0].firstChild.nodeValue )

                        #self.status_ = initstatus

                        for contact in contactsDom :
                            contactIP = contact.getElementsByTagName('ip')[0].firstChild.nodeValue
                            contactNick = contact.getElementsByTagName('nick')[0].firstChild.nodeValue
                            contactSubnick = contact.getElementsByTagName('subnick')[0].firstChild.nodeValue
                            contactAvatar = contact.getElementsByTagName('avatar')[0].firstChild.nodeValue
                            contactUser = contact.getElementsByTagName('user')[0].firstChild.nodeValue
                            contactStatus = int ( contact.getElementsByTagName('status')[0].firstChild.nodeValue )
                            contactStamp = int ( contact.getElementsByTagName('stamp')[0].firstChild.nodeValue )
                            contactPort = 1864

                            user = {}
                            user['ip'] = contactIP
                            user['localip'] = self.contacts[contactUser]['localip']
                            user['user'] = contactUser
                            user['nick'] = contactNick
                            user['subnick'] = contactSubnick
                            user['port'] = contactPort
                            user['avatar'] = contactAvatar
                            user['status'] = contactStatus
                            user['stamp'] = contactStamp
                            user['connected'] = self.contacts[contactUser]['connected']

                            #info_refresh ( user ) ;

                            self.contacts[contactUser] = user
                            self.on_refresh ( user )

                        datasDom = doc.getElementsByTagName('data')
                        for data in datasDom:
                            print data.toxml()
                            content = data.getElementsByTagName('content')[0].firstChild.nodeValue
                            self.send_function( content )
                            if self.debug>2: print data.toxml()
                            if self.debug>2: print "C %s" % (content)

                        self.cerror = None
                        if self.debug>1:  print "[http] OK"

                    else:
                        self.cerror = error.AUTH
                        if self.debug>0:  print "[http] AUTH ERR"
                        return 0

                    doc.unlink()

            else:
                self.cerror = error.CONN
                if self.debug>0:  print "[http] CONN ERR: %s" % (response.reason)
                return 0
            
