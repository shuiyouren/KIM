class login:
    "Login with the Emsene server"
    def __init__(self, user, host, debug=0):
        self.user = user
        self.debug = debug
        self.host = host

        epassphrase = stepOne ()


    def stepOne (self):

        debug = self.debug
        user = self.user
        host = self.host

        try:
            serverconn = httplib.HTTPConnection( host , 80, 10)
            params = urllib.urlencode({'user': user, 'request': 'login', 'info': 'yes'})
            serverconn.request("GET", '/eserver/connection/?%s' % params)
        except:
            cerror = error.CONN
            if debug>0:  print "[eserver] CONN ERR"
            return 0
        else:
            try:
                response = serverconn.getresponse()
            except:
                cerror = error.CONN
                if debug>0:  print "[eserver] CONN ERR"
                serverconn.close()
                return 0
            serverconn.close()

            if response.reason=="OK":
                try:
                    doc = xml.dom.minidom.parseString( response.read() )
                except:
                    cerror = error.DATA
                else:
                    error_ = doc.getElementsByTagName('error')[0].firstChild.nodeValue

                    if error_ == 'ok':

                        info_function != None: info_function ( 1 ) #'Processing list...'

                        epassphrase = doc.getElementsByTagName('epassphrase')[0].firstChild.nodeValue

                        cerror = None
                        if debug>1:  print "[eserver] OK: "+user

                    else:
                        cerror = error.AUTH
                        if debug>0:  print "[eserver] AUTH ERR"
                        return 0

                    doc.unlink()
            else:
                cerror = error.CONN
                if debug>0:  print "[eserver] CONN ERR"
                return 0
        return 1
