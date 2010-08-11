class process:
    def __init__(self):
        pass

    def process_data (self, data):
        if not data:
            return
        #print "  [eclient] receivingData: "+data
        try:
            doc = xml.dom.minidom.parseString( data )
        except:
            if self.debug>0: print "   [eclient] Invalid XML from client."
            return '<eserver><!-- BadXML --><eserver><status>error</status></eserver>'

        type_ = doc.getElementsByTagName('type')[0].firstChild.nodeValue

        if self.debug>1: print "   [eclient] Request Type: %s" % type_

        if type_=='message':
            sender = doc.getElementsByTagName('sender')[0].firstChild.nodeValue
            body = doc.getElementsByTagName('body')[0].firstChild.nodeValue
            self.on_message ( body, sender)
            doc.unlink()
            return "ok"
        elif type_=='status_request':
            if self.debug>1: print "    [eclient] To %s" % doc.getElementsByTagName('recipient')[0].firstChild.nodeValue  
            if doc.getElementsByTagName('recipient')[0].firstChild.nodeValue == self.user:
                if self.debug>1: print "    [eclient] Status Request" 
                if self.debug>1: print "request of %s to %s" % ( doc.getElementsByTagName('recipient')[0].firstChild.nodeValue, self.user )

                doc.unlink()

                if self.debug>1: print "    [eclient] Status: %s" % self.status_

                if self.status_ == status.BUSY:
                    mystatus = 'busy'
                elif self.status_ == status.AWAY:
                    mystatus = 'away'
                elif self.status_ == status.IDLE:
                    mystatus = 'idle'
                elif self.status_ == status.ONLINE:
                    mystatus = 'online'
                else:
                    return

                send = StringIO()
                send.write ('<connection>')
                send.write (' <type>status_answer</type>')
                send.write (' <pstatus>%s</pstatus>' % mystatus)
                send.write (' <user>%s</user>' % self.user)
                send.write (' <nick>%s</nick>' % self.nick)
                send.write (' <subnick>%s</subnick>' % self.subnick)
                send.write ('</connection>')
                send.seek(0)

                if self.debug>2: print "    [eclient] Answer: %s" % send.read()
                return send.read()
            else:
                return '<eserver><!-- Not Recipient --><status>error</status></eserver>'
