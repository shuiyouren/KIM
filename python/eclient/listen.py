import threading, time, sys
from socket import *

class listen(threading.Thread):
    def __init__(self, port, socket, send_function ):
        threading.Thread.__init__(self)
        self.socket = socket
        self.send_function = send_function
        self.debug = 0
        self.simultaneus = 50
        self.port = port
        self.maxconn = 50
        
    def run (self):
        data = None
        self.socket.settimeout ( None )
        unconnected=1

        while unconnected:
            if self.debug>1: print "[listen] Openning port %s" % self.port
            unconnected=0
            try:
                self.socket.bind(( '', self.port)) #connect to port
            except:
                if self.debug>2: print "[listen] Port error: %s" % sys.exc_info()[0]
                unconnected=1
                time.sleep(0.5)

        if self.debug>0: print ( "[listen] Ready" )

        self.socket.listen( self.maxconn ) #set max connections

        while 1:
            if self.debug>1: print "[listen] Listening"
            try:
                connection, address = self.socket.accept()
            except:
                continue
            if self.debug>1: print "[listen] Connected to %s" % str( address )
            receiving_ = receiving( self.socket, connection, self.send_function )
            receiving_.debug = self.debug
            receiving_.start()


class receiving(threading.Thread):

    def __init__(self, socket,  connection, send_function ):
        threading.Thread.__init__(self)
        self.socket = socket
        self.connection = connection
        self.send_function = send_function
        self.debug = 0

    def run (self):
        data = None

        if self.debug>1: print "[listen] Receiving"
        data = self.connection.recv(1024)
        if self.debug>1: print "[listen] Received: %s" % data
        send =  self.send_function( data )
        if send:
            self.connection.send ( send )
        self.connection.close()
        #self.socket.close
