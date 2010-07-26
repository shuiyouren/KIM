import urllib, httplib, xml.dom.minidom, binascii, base64
from base import *
from rc4 import rc4

class login:
    "Login with the Emsene server"
    def __init__(self):
        self.user = "test1"
        self.password = "test1"
        self.host = "www.eibriel.com"
        self.debug = 1
        #self.info_function = info_function

        debug = self.debug

        if debug>0:  print "[login] Initializing"

        #self.info_function ( 0 )
        passphrase = self._stepOne ()

        if not self.error_: suid = self._stepTwo ( passphrase )
        #if debug>0:  print "[login] --Suid : %s" % suid
        #self.info_function ( 1 )

    def _stepOne (self):

        debug = self.debug
        user = self.user
        host = self.host

        if debug>0:  print "[login] -Step One User: %s Host: %s" % (user, host)

        req = '''<input>
<erequests>
  <erequest type="auth_node">
  <body>
   <subtype>step1</subtype>
   <user>test1</user>
  </body>
  </erequest>
 </erequests>
</input>'''

        params = urllib.urlencode({'erequest': req })
        response = self._http_send ( host, params)
        if response:
            doc = self._get_xml ( response.read() )
            if doc:
                print doc.toxml ()
                if len(doc.getElementsByTagName('eresponse')) == 0 :
                    self.error_ = error.AUTH
                    return 0
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
            if debug>0 and response != 0:  print "[login] CONN ERR 3 %s" % response.reason
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

        req = '''<input>
<erequests>
  <erequest type="auth_node">
  <body>
   <subtype>step2</subtype>
   <user>test1</user>
   <passphrase_md5>'''+pass_md5+'''</passphrase_md5>
  </body>
  </erequest>
 </erequests>
</input>'''

        params = urllib.urlencode({'erequest': req})
        response = self._http_send ( host, params)
        if response:
            doc = self._get_xml ( response.read() )
            print doc.toxml ()
            if doc:
                esuid = str(doc.getElementsByTagName('esuid')[0].firstChild.nodeValue)
                if debug>0:  print "[login] --Esuid : %s" % esuid
                #if debug>0:  print "[login] --passphrase : %s" % passphrase
                encrypter = rc4 ()
                k = encrypter.initialize ( passphrase )
                bin = binascii.unhexlify( esuid )

                #if debug>0:  print "[login] ---Esuid_bin : %s" % bin

                suid = encrypter.run_rc4(k, bin)
                #if debug>0:  print "[login] ---Suid_64 : %s" % suid_64

                #suid = base64.b64decode ( suid_64 )
                if debug>0:  print "[login] --Suid : %s" % suid
                return suid

    def _http_send ( self, host, params ):
        debug = self.debug

        try:
            serverconn = httplib.HTTPConnection( host, 80, 10)
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            serverconn.request("POST", '/eserver/index-sample.php', params, headers)
        except:
            self.error_ = error.CONN
            if debug>0:  print "[login] CONN ERR 1"
            return 0
        else:
            try:
                response = serverconn.getresponse()
            except:
                self.error_ = error.CONN
                if debug>0:  print "[login] CONN ERR 2"
                serverconn.close()
                return 0
            serverconn.close()

            if response.reason=="OK":
                return response
            else:
                self.error_ = error.CONN
                return response

    def _get_xml ( self, data):
        debug = self.debug

        try:
            doc = xml.dom.minidom.parseString( data )
        except:
            self.error_ = error.DATA
            if debug>0:  print "[login] DATA ERR %s" % data
            return
        else:
            #error_ = doc.getElementsByTagName('status')[0].firstChild.nodeValue
            error_ = 'ok'
            if error_ == 'ok':
                return doc

log = login ()
