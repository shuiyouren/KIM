from socket import *

class kimConn:
            def __init__(self, Ip, Port):
                self.socket = None
                self.connected = False
                self.error = ''
                self.connected = True
                self.connect (Ip, Port)
            def connect (self, Ip, Port ):
                self.Ip = Ip
                self.Port = Port
                self.socket = socket(AF_INET, SOCK_STREAM)
                try:
                    self.socket.connect((self.Ip, self.Port))
                except:
                    self.error = 'error'
                    return False
                self.connected = True
                return True
            def send (self, data):
                while self.connected == False:
                    #wait
                    h=1
                tries = 0
                trya = True
                while (trya) and (tries < 50):
                    trya = False
                    try:
                        self.socket.send ( data )
                        self.error = ''
                    except:
                        tries = tries + 1
                        trya = True
                        self.error = 'error'
                if self.error == 'error':
                    return False
                return True
            
            def recv ( self, cache ):
                return self.socket.recv( cache)
                
            def close (self):
                if self.socket != None:
                    self.socket.close()
                return True
