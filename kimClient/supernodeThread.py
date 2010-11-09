from supernodeListening import *

class supernodeThread:
    def __init__(self, port, host, server_name, sessionid):
        self.port = port
        self.host = host
        self.server_name = server_name
        self.sessionid = sessionid
        self.jobs = list ()
        self.running = True
        self.notificationFunction = None
        
        print 'Create supernodeThread'
        self.listening = supernodeListening (self.port, self.host, self.server_name, self.sessionid)
        self.listening.start()
        print 'End supernodeThread'
        
    def onNotification ( self, notificationFunction ):
        self.notificationFunction = notificationFunction
        self.listening.notificationFunction = notificationFunction
        
    def notify ( self, note ):
        if self.notificationFunction != None:
            self.notificationFunction ( note )
        
    def stop (self):
        print "supernodeListening Stop"
        self.listening.stop()
