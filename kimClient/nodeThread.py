from nodeConnection import *

class nodeThread:
    def __init__(self, port, host, server_name, sessionid):
        self.port = port
        self.host = host
        self.server_name = server_name
        self.sessionid = sessionid
        self.jobs = list ()
        self.running = True
        print 'Create supernodeThread'
        self.connection = nodeConnection (self.port, self.host, self.server_name, self.sessionid)
        self.connection.start()
        #print 'End supernodeThread'
        
    def send (self, data):
        self.connection.send ( data )    
    
    def stop (self):
        print "supernodeListening Stop"
        self.connection.close()
