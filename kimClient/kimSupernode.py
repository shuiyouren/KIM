from serverAuth import *
from supernodeThread import *

class kimSupernode:
    def __init__(self, supernode_port, server_port, server_name, server_host, username, password):
    
        self.supernode_port = supernode_port
        self.server_port = server_port
        self.server_name = server_name
        self.server_host = server_host
        self.username = username
        self.password = password
        self.notificationFunction = None
        self.kisupernode = None
        
        
    def authorize (self):
        self.auth = serverAuth(self.server_host, self.server_port, self.server_name, self.username, self.password)
        self.sessionid = self.auth.execute ()
        
        if self.sessionid == False:
            self.notify ( 'auth-fail' )
            return
        
        self.notify ( 'authorized' )
        
    def start (self):
        self.kisupernode = supernodeThread( self.supernode_port, self.server_host, self.server_name, self.sessionid )
        
    def onNotification ( self, notificationFunction ):
        self.notificationFunction = notificationFunction
        if self.kisupernode != None:
            self.kisupernode.notificationFunction = notificationFunction
        
    def notify ( self, note ):
        if self.notificationFunction != None:
            self.notificationFunction ( note )
        
    def stop (self):
        print "supernodeThread STOP"
        try:
            self.kisupernode.stop()
        except:
            return
