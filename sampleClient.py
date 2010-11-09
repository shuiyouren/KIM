#!/usr/bin/python
# -*- coding: utf-8 -*-

from kimClient import *
import string

class sampleClient ():
    def __init__ (self):
        self.server_port = 5333
        self.supernode_port = 5334
        self.server_name = 'kimly.org'
        #self.server_host = 'kimly.org'
        self.server_host = 'localhost'
        self.supernode_host = 'localhost'
        self.authorized = False

        print "User?: Eibriel"
        self.username = 'eibriel'
        print "Pass?:"
        self.password='eibriel'

        print "Loading Supernode"

        self.Supernode = kimSupernode (self.supernode_port, self.server_port, self.server_name, self.server_host, self.username, self.password )
        self.Supernode.onNotification ( self.onSupernodeNotification )
        print "[client] Authorizing Supernode"
        self.Supernode.authorize()

        if not self.authorized:
            print "[client] Exiting cause an Authorization error"
            return
        print "[client] Starting Supernode"
        self.Supernode.start()

            
        self.Node = kimNode (self.supernode_port, self.supernode_host, self.server_port, self.server_name, self.server_host, self.username, self.password )

        self.Node.handleOnBuddyChange ( self.onBuddyChange )
        self.Node.handleOnMessageReceiving ( self.onMessageReceiving )

        value = ''
        while 1:
            value = raw_input("@%s :" % self.username)
            if value == '': continue
            if value == '!exit': break
            #print value[0]
            if value[0] == '@':
                #print "Mess"
                to = string.split( value, ' ', 1 )[0][1:]
                message = string.split( value, ' ', 1 )[1]
                self.Node.sendMessage( to, message)
            #Node.send()

        print "[client] Stopping Supernode"
        self.Supernode.stop()
        print "[client] Supernode stoped?"
        

    def onSupernodeNotification(self, notification):
        if notification=='authorized':
            print "[client] Supernode Authorized"
            self.authorized = True
        elif notification=='auth-fail':
            print "[client] Supernode NOT Authorized"
            self.authorized = False
        elif notification=='stoped':
            print "[client] Supernode Stoped"
            
    def onBuddyChange(self, buddy, action, value):
        '''Buddy changing'''
        print "[client] New status %s %s: %s" % (buddy, action, value)

    def onMessageReceiving(self, from_, to, body, type_):
        '''Message Receiving'''
        print "[client] Message %s from %s to %s: %s" % (type_, from_, to, body)
    
client = sampleClient ()
