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
    
        self.auth = serverAuth(server_host, server_port, server_name, username, password)
        self.sessionid = self.auth.execute ()
        
        self.kisupernode = supernodeThread( self.supernode_port, self.server_host, self.server_name, self.sessionid )
        
    def stop (self):
        print "supernodeThread STOP"
        self.kisupernode.stop()
