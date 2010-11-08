class serverJob(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.type = connection
        self.jid = address
        self.data = list ()
    def run (self):
        if self.type == 'auth-n':
            print 'auth-n'
        if self.type == '':
            print 'auth-sn'
        if self.type == 'get-supernodes':
            print 'get-supernodes'
