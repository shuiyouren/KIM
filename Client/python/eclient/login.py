import urllib, httplib, xml.dom.minidom, binascii, base64
from base import *
from rc4 import rc4

class login:
    "Login with the Emsene server"
    def __init__(self, user, password, host, debug=0, info_function=None):
        self.user = user
        self.password = password
        self.host = host
        self.debug = debug
        self.info_function = info_function

        if debug>0:  print "[login] Initializing"

        self.info_function ( 0 )
        passphrase = self._stepOne ()

        if not self.error_: suid = self._stepTwo ( passphrase )
        self.info_function ( 1 )

    def _stepOne (self):

        debug = self.debug
        user = self.user
        host = self.host

        if debug>0:  print "[login] -Step One User: %s Host: %s" % (user, host)

        params = urllib.urlencode({'user': user, 'request': 'login'})
        response = self._http_send ( host, params)
        if response:
            doc = self._get_xml ( response.read() )
            if doc:

                epassphrase = doc.getElementsByTagName('epassphrase')[0].firstChild.nodeValue

                if debug>0:  print "[login] -Epassphrase: %s" % epassphrase

                encrypter = rc4 ()

                if debug>0:  print "[login] -RC4 Pass: %s" % self.password

                k = encrypter.initialize ( self.password )

                #Test
                if 0:
                    test = encrypter.run_rc4(k, 'Maria Sol', 1)

                    if debug>0:  print "[login] --Test Bin: %s" % test

                    test_hex = binascii.hexlify( test )

                    if debug>0:  print "[login] --Test Hex: %s" % test_hex

                    test_res = encrypter.run_rc4(k, test, 1)

                    if debug>0:  print "[login] --Test Res: %s" % test_res

                if debug>0:  print "[login] --Initialized"

                bin = binascii.unhexlify( epassphrase )

                #if debug>0:  print "[login] --Unhexlify: %s" % bin

                passphrase = encrypter.run_rc4(k, bin, 1)
                #passphrase = binascii.unhexlify( passphrase )

                if debug>0:  print "[login] --Passphrase: %s" % passphrase

                self.error_ = None

            else:
                self.error_ = error.AUTH
                doc.unlink()
                if debug>0:  print "[login] AUTH ERR"
                return 0

            doc.unlink()
        else:
            self.error_ = error.CONN
            if debug>0:  print "[login] CONN ERR 3 %s" % response.reason
            return 0
        return passphrase

    def _stepTwo (self, passphrase):
        import hashlib
        debug = self.debug
        user = self.user
        host = self.host

        if debug>0:  print "[login] -Step Two"

        pass_md5 = hashlib.md5( passphrase ).hexdigest()

        if debug>0:  print "[login] --Passphrase MD5: %s" % pass_md5

        params = urllib.urlencode({'user': user, 'request': 'suid', 'passphrase_md5':pass_md5})
        response = self._http_send ( host, params)
        if response:
            doc = self._get_xml ( response.read() )
            if doc:
                esuid = doc.getElementsByTagName('esuid')[0].firstChild.nodeValue
                if debug>0:  print "[login] --Esuid : %s" % esuid

                encrypter = rc4 ()
                k = encrypter.initialize ( passphrase )
                bin = binascii.unhexlify( esuid )

                if debug>0:  print "[login] ---Esuid_bin : %s" % bin

                suid = encrypter.run_rc4(k, bin, 1)
                #if debug>0:  print "[login] ---Suid_64 : %s" % suid_64

                #suid = base64.b64decode ( suid_64 )
                if debug>0:  print "[login] --Suid : %s" % suid
                return suid

    def _http_send ( self, host, params ):
        debug = self.debug

        try:
            serverconn = httplib.HTTPConnection( host , 80, 10)
            serverconn.request("GET", '/eserver/connection/?%s' % params)
        except:
            self.error_ = error.CONN
            if debug>0:  print "[login] CONN ERR 1"
            return
        else:
            try:
                response = serverconn.getresponse()
            except:
                self.error_ = error.CONN
                if debug>0:  print "[login] CONN ERR 2"
                serverconn.close()
                return
            serverconn.close()

            if response.reason=="OK":
                return response

    def _get_xml ( self, data):
        try:
            doc = xml.dom.minidom.parseString( data )
        except:
            self.error_ = error.DATA
            if debug>0:  print "[login] DATA ERR %s" % data
            return
        else:
            error_ = doc.getElementsByTagName('error')[0].firstChild.nodeValue
            if error_ == 'ok':
                return doc


