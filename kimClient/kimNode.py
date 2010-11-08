from serverAuth import *
from nodeThread import *

class kimNode:
    def __init__(self, supernode_port, supernode_host, server_port, server_name, server_host, username, password):
    
        self.supernode_port = supernode_port
        self.supernode_host = supernode_host
        self.server_port = server_port
        self.server_name = server_name
        self.server_host = server_host
        self.username = username
        self.password = password
    
        self.auth = serverAuth(server_host, server_port, server_name, username, password)
        self.sessionid = self.auth.execute ()
        
        self.kinode = nodeThread( self.supernode_port, self.supernode_host, self.server_name, self.sessionid )
        
    def handleOnBuddyChange (self, function):
        ''''''
        
    def handleOnMessageReceiving (self, function):
        ''''''
        
    def sendMessage (self, to, value):
        print "mess"
        self.kinode.send( '<message to="%s" from="%s">%s</message>' % (to, self.username, value) )
        
    def stop (self):
        print "nodeThread STOP"
        self.kinode.stop()
