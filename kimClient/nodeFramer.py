import threading
import time

class nodeFramer (threading.Thread):
    def __init__(self, snodeconn):
        threading.Thread.__init__(self)
        self.snodeconn = snodeconn
        self.Tosend = ''
        self.sleeptime = 1.5
    def run (self):
        while 1:
            time.sleep ( self.sleeptime )
            if self.Tosend=='':
                self.Tosend = "<iq type='ping'>"
            #else:
                #print Tosend
            #print "Tosend: %s" % self.Tosend
            self.snodeconn.send (self.Tosend)
            self.Tosend = ''
            
    def addToSend (self, toSend):
        self.Tosend = "%s%s" % (self.Tosend, toSend)
